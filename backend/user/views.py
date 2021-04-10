from django.http.response import HttpResponseNotModified
from .serializers import user_details_serializer,cart_products_serializer,order_serializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import details,deleted_accounts,cart,orders
from product.models import details as product_details
from retailer.models import product_sold
from retailer.models import details as retailer_details
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login as django_login,logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class SignUpUser(APIView):

    def post(self,request):
        data=request.data
        if not details.objects.filter(email=data["email"],phone_number=data["phone_number"]).exists():
            user_serializer=user_details_serializer(data=data)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                return Response(status=201)
            return Response(status=400)
        return Response(status=400)

    def get(self,request):
        return Response(status=405)

class DeleteUser(APIView):
    authentication_classes=[TokenAuthentication]
    def post(self,request):
        data=request.data
        if details.objects.filter(email=data["email"],password=data["password"]).exists():
            user=details.objects.get(email=data["email"],password=data["password"])
            deleted_user=deleted_accounts.objects.create(name=user.name,
                                                        email=user.email,password=user.password,
                                                        phone_number=user.phone_number,house_no=user.house_no,
                                                        society=user.society,nearby=user.nearby,street=user.street,
                                                        pincode=user.pincode,area=user.area,city=user.city,state=user.state)
            deleted_user.save()
            user.delete()
            return Response(status=200)
        else:
            return Response(status=404)
        
    def get(self,request):
        return Response(status=405)

class UpdateInfoUser(APIView):
    authentication_classes=[TokenAuthentication]
    def post(self,request):
        data=request.data
        if details.objects.filter(email=data["email"],password=data["password"]).exists():
            user=details.objects.get(email=data["email"],password=data["password"])
            user.name=data["name"]
            user.email=data["email"]
            user.password=data["password"]
            user.house_no=data["house_no"]
            user.society=data["society"]
            user.nearby=data["nearby"]
            user.street=data["street"]
            user.pincode=data["pincode"]
            user.area=data["area"]
            user.city=data["city"]
            user.state=data["state"]
            user.save()
            return Response(status=200)
        
        else:
            return Response(status=404)
            
    def get(self,request):
        data=request.data
        if details.objects.filter(email=data["email"],password=data["password"]).exists():
            user=details.objects.get(email=data["email"],password=data["password"])
            user_serializer=user_details_serializer(user)
            return Response(user_serializer.data,status=200)

class GetCartInfo(APIView):
    authentication_classes=[TokenAuthentication]
    def get(self,request):
        data=request.data
        cart_products=cart.objects.filter(user=data["id"])
        cart_serializer=cart_products_serializer(cart_products,many=True)
        return Response(cart_serializer.data,status=200)

    def post(self,request):
        return Response(status=405)

class AddIntoCart(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        data=request.data
        user=details.objects.get(id=data["id"])
        product=product_details.objects.get(id=data["product_id"])
        cart_product=cart.objects.create(user=user,product_details=product)
        cart_product.save()
        return Response(status=201)

    def get(self,request):
        return Response(status=405)

class DeleteFromCart(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        data=request.data
        if cart.objects.filter(id=data["cart_id"]).exists():
            cart_obj=cart.objects.get(id=data["cart_id"])
            cart_obj.delete()
            return Response(status=202)
        return Response(status=404)
    
    def get(self,request):
        return Response(status=405)

class GetOrderInfo(APIView):
    authentication_classes=[TokenAuthentication]
    
    def get(self,request):
        data=request.data
        user=user=details.objects.get(id=data["id"])
        if orders.objects.filter(user=user).exists():
            order=orders.objects.filter(user=user)
            order_ser=order_serializer(order,many=True)
            return Response(order_ser.data,status=200)
        return Response(status=404)
    
    def post(self,request):
        return Response(status=405)
        

class PlaceOrder(APIView):
    authentication_classes=[TokenAuthentication]
    def post(self,request):
        data=request.data
        user=details.objects.get(id=data["id"])
        product=product_details.objects.get(id=data["product_id"])
        retailer=retailer_details.objects.get(id=data["retailer_id"])

        if product_sold.objects.filter(retailer=data["retailer_id"],product=data["product_id"]).exists():
            product_sold_prev=product_sold.objects.get(retailer=data["retailer_id"])
            product_sold_prev.product_pieces=int(product_sold_prev.product_pieces)+1
            product_sold_prev.save()
        else:
            product_sold_obj=product_sold.objects.create(retailer=retailer,product=product,product_pieces="1")
            product_sold_obj.save()
        order=orders.objects.create(user=user,product_details=product)
        order.save()
        
        return Response(status=201)
    
    def get(self,request):
        return Response(status=405)

class CancelOrder(APIView):
    authentication_classes=[TokenAuthentication]
    def post(self,request):
        data=request.data
        if orders.objects.filter(id=data["order_id"]).exists():
            if product_sold.objects.filter(retailer=data["retailer_id"],product=data["product_id"]).exists():
                product_sold_prev=product_sold.objects.get(retailer=data["retailer_id"])
                product_sold_prev.product_pieces=int(product_sold_prev.product_pieces)-1
                product_sold_prev.save()
            else:
                return Response(status=404)
            order=orders.objects.get(id=data["order_id"])
            order.delete()
            return Response(status=202)
        return Response(status=404)
    
    def get(self,request):
        return Response(status=405)
    
class LoginUser(APIView):

    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        django_login(request,user)
        token,created=Token.objects.get_or_create(user=user)
        return Response({"key":str(token)})
    
    def get(self,request):
        return Response(status=405)

class LogoutUSer(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        django_logout(request)
        return Response(status=200)
    
    def get(self,request):
        return Response(status=405)