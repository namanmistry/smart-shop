from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from os.path import join
from rest_framework.response import Response
from .models import details,catagory, review
from retailer.models import details as retailer_details
from user.models import details as user_details,orders
import random
from .serializers import product_serializer,review_serialzer,catagory_serializer
import os
from django.db.models import Q
from django.http import JsonResponse

BASE_DIR=Path(__file__).resolve().parent.parent
# Create your views here.
class AddNewProduct(APIView):

    def post(self,request):
        data=request.data
        uploaded_photo=request.FILES['photo']
        uploaded_video=request.FILES['video']
        retailer_detail=retailer_details.objects.get(id=data["retailer_details"])
        catagory_details=catagory.objects.get(name=data["catagory_name"])
        fs=FileSystemStorage(join(BASE_DIR,'photos_videos'))
        uploaded_photo_name=uploaded_photo.name
        uploaded_video_name=uploaded_video.name
        random_number=random.randint(10**(10-1),10**10-1)

        if details.objects.filter(img_name=uploaded_photo_name).exists():
            name_list_photo=uploaded_photo_name.split('.')
            uploaded_photo_name=uploaded_photo_name+str(random_number)+"."+name_list_photo[len(name_list_photo)-1]
        
        if details.objects.filter(video_name=uploaded_video_name).exists():
            name_list_video=uploaded_video_name.split('.')
            uploaded_video_name=uploaded_video_name+str(random_number)+"."+name_list_video[len(name_list_video)-1]
        product=details.objects.create(product_catagory=catagory_details,name=data["name"],
                                        img_name=uploaded_photo_name,video_name=uploaded_video_name,
                                        price=data["price"],description1=data["description1"],
                                        description2=data["description2"],description3=data["description3"],
                                        retailer_details=retailer_detail)
        fs.save(uploaded_photo_name,uploaded_photo)
        fs.save(uploaded_video_name,uploaded_video)
        product.save()
        return Response(status=200)

    def get(slef,request):
        return Response(status=405)
        
class DeleteProduct(APIView):

    def post(self,request):
        data=request.data
        if details.objects.filter(id=data["id"]).exists():
            product=details.objects.get(id=data["id"])
            os.remove(f'''{BASE_DIR}/photos_videos/{product.img_name}''')
            os.remove(f'''{BASE_DIR}/photos_videos/{product.video_name}''')
            product.delete()
            return Response(status=202)
        return Response(status=404)
    
    def get(slef,request):
        return Response(status=405)

class GetProductsByRetailerId(APIView):

    def get(self,request):
        data=request.data
        retailer=retailer_details.objects.get(id=data["id"])
        products=details.objects.filter(retailer_details=retailer)
        serializer=product_serializer(products,many=True)
        serializer.data[0]["img_name"]='/static/'+serializer.data[0]["img_name"]+"/"
        serializer.data[0]["video_name"]='/static/'+serializer.data[0]["video_name"]+"/"
        return Response(serializer.data,status=200)

    def post(self,request):
        return Response(status=405)

class GetProductsByCatagory(APIView):

    def get(self,request):
        data=request.data
        catagory_object=catagory.objects.get(name=data["name"])
        products=details.objects.filter(product_catagory=catagory_object)
        serializer=product_serializer(products,many=True)
        serializer.data[0]["img_name"]='/static/'+serializer.data[0]["img_name"]+"/"
        serializer.data[0]["video_name"]='/static/'+serializer.data[0]["video_name"]+"/"
        return Response(serializer.data,status=200)

    def post(self,request):
        return Response(status=405)

class GetProductsBySearch(APIView):
    
    def get(self,request):
        data=request.data
        if details.objects.filter(Q(name__icontains=data["query"])|Q(description1__icontains=data["query"])|Q(price__icontains=data["query"])).exists():
            products=details.objects.filter(Q(name__icontains=data["query"])|Q(description1__icontains=data["query"])|Q(price__icontains=data["query"]))
            product_ser=product_serializer(products,many=True)
            return Response(product_ser.data,status=200)
        return Response(status=404)
    
    def post(self,request):
        return Response(status=405)
    
class AddReview(APIView):

    def post(self,request):
        data=request.data
        user=user_details.objects.get(id=data["id"])
        product=details.objects.get(id=data["product_id"])
        review_obj=review(user=user,description=data["description"],star=data["star"],product=product)
        review_obj.save()

    def get(slef,request):
        return Response(status=405)

class GetReviewsByProductId(APIView):

    def get(self,request):
        data=request.data
        product=details.objects.get(id=data["product_id"])
        if review.objects.filter(product=product).exists():
            reviews=review.objects.filter(product=product)
            review_ser=review_serialzer(reviews,many=True)
            return Response(review_ser.data,status=200)
        return Response(status=404)

class GetOrderInvoice(APIView):

    def get(self,request):
        data=request.data
        user=user_details.objects.get(id=data["id"])
        if orders.objects.filter(user=user).exists():
            order_details=orders.objects.filter(user=user)
            product_list=[]
            struct={}
            struct_total={}
            grand_total=0
            for i in order_details:
                product=details.objects.get(id=i.product_details.id)
                struct["name"]=product.name
                struct["price"]=product.price
                grand_total=grand_total+int(product.price)
                product_list.append(struct)
            struct_total["total"]=grand_total
            product_list.append(struct_total)
            return JsonResponse(product_list,safe=False)
        return Response(status=404)

    def post(self,request):
        return Response(status=405)

class DefaultHomeProducts(APIView):

    def get(self,request):
        products=details.objects.all()[:9]
        product_ser=product_serializer(products,many=True)
        for i in product_ser.data:
            i["img_name"]='/static/'+i["img_name"]+"/"
            i["video_name"]='/static/'+i["video_name"]+"/"
        return Response(product_ser.data,status=200)
    
    def post(self,request):
        return Response(status=405)

class DefaultHomeCatagory(APIView):

    def get(self,request):
        ctatagories=catagory.objects.all()[:4]
        catagory_ser=catagory_serializer(ctatagories,many=True)
        return Response(catagory_ser.data,status=200)
        
    def post(self,request):
        return Response(status=405)

class AllCatagories(APIView):

    def get(self,request):
        catagories=catagory.objects.all()
        catagory_ser=catagory_serializer(catagories,many=True)
        return Response(catagory_ser.data,status=200)

    def post(self,request):
        return Response(status=405)

