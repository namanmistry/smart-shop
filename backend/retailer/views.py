from .serializers import retailer_details_serializer, product_sold_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import details, deleted_accounts, product_sold
from user.models import orders
from user.serializers import order_serializer
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login as django_login, logout as django_logout

class SignUpRetailer(APIView):

    def post(self, request):
        data = request.data
        if not details.objects.filter(email=data["email"], phone_number=data["phone_number"]).exists():
            user_serializer = retailer_details_serializer(data=data)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                return Response(status=201)
            return Response(status=400)
        return Response(status=400)

    def get(self, request):
        return Response(status=405)


class DeleteRetailer(APIView):

    def post(self, request):
        data = request.data
        if details.objects.filter(email=data["email"], password=data["password"]).exists():
            retailer = details.objects.get(
                email=data["email"], password=data["password"])
            deleted_retailer = deleted_accounts.objects.create(shop_name=retailer.name,
                                                               email=retailer.email, password=retailer.password,
                                                               phone_number=retailer.phone_number, shop_no=retailer.house_no,
                                                               society=retailer.society, nearby=retailer.nearby, street=retailer.street,
                                                               pincode=retailer.pincode, area=retailer.area, city=retailer.city, state=retailer.state)
            deleted_retailer.save()
            retailer.delete()
            return Response(status=200)
        else:
            return Response(status=404)

    def get(self, request):
        return Response(status=405)


class UpdateInfoRetailer(APIView):

    def post(self, request):
        data = request.data
        if details.objects.filter(email=data["email"], password=data["password"]).exists():
            retailer = details.objects.get(
                email=data["email"], password=data["password"])
            retailer.shop_name = data["shop_name"]
            retailer.email = data["email"]
            retailer.password = data["password"]
            retailer.shop_no = data["shop_no"]
            retailer.society = data["society"]
            retailer.nearby = data["nearby"]
            retailer.street = data["street"]
            retailer.pincode = data["pincode"]
            retailer.area = data["area"]
            retailer.city = data["city"]
            retailer.state = data["state"]
            retailer.save()
            return Response(status=200)

        else:
            return Response(status=404)

    def get(self, request):
        data = request.data
        if details.objects.filter(email=data["email"], password=data["password"]).exists():
            retailer = details.objects.get(
                email=data["email"], password=data["password"])
            retailer_serializer = retailer_details_serializer(retailer)
            return Response(retailer_serializer.data, status=200)


class GetProductSoldInfo(APIView):

    def get(self, request):
        data = request.data
        retailer = details.objects.get(id=data["retailer_id"])
        if product_sold.objects.filter(retailer=retailer).exists():
            product_sold_info = product_sold.objects.filter(retailer=retailer)
            product_sold_info_serializer = product_sold_serializer(
                product_sold_info, many=True)
            return Response(product_sold_info_serializer.data, status=200)
        return Response(status=404)


class GetOrderDetailsForRetailer(APIView):

    def get(self, request):
        data = request.data
        retailer = details.objects.get(id=data["retailer_id"])
        if orders.objects.filter(retailer_details=retailer).exists():
            order_details = orders.objects.filter(retailer_details=retailer)
            order_details_ser = order_serializer(order_details, many=True)
            return Response(order_details_ser.data, status=200)
        return Response(status=404)

    def post(self, request):
        return Response(status=405)

class LoginRetailer(APIView):

    def post(self,request):
        data=request.data
        if details.objects.filter(email=data["email"],password=data["password"]).exists():
            return Response(status=200)
        return Response(status=403)
    
    def get(self,request):
        return Response(status=405)
        
        
