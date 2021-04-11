from .serializers import user_details_serializer, cart_products_serializer, order_serializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import details, deleted_accounts, cart, orders, login_log
from product.models import details as product_details
from retailer.models import product_sold
from retailer.models import details as retailer_details
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class SignUpUser(APIView):
    '''View that signs up a new user through post request.'''
    def post(self, request):
        data = request.data
        if not details.objects.filter(email=data["email"], phone_number=data["phone_number"]).exists():
            user_serializer = user_details_serializer(data=data)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
                return Response(status=201)
            return Response(status=400)
        return Response(status=400)

    def get(self, request):
        return Response(status=405)


class DeleteUser(APIView):
    '''View that deletes a user if it exists in database through post request.'''
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self, request):
        data = request.data
        if details.objects.filter(email=data["email"], password=data["password"]).exists():
            user = details.objects.get(
                email=data["email"], password=data["password"])
            deleted_user = deleted_accounts.objects.create(name=user.name,
                                                           email=user.email, password=user.password,
                                                           phone_number=user.phone_number, house_no=user.house_no,
                                                           society=user.society, nearby=user.nearby, street=user.street,
                                                           pincode=user.pincode, area=user.area, city=user.city, state=user.state)
            deleted_user.save()
            user.delete()
            return Response(status=200)
        else:
            return Response(status=404)

    def get(self, request):
        return Response(status=405)


class UpdateInfoUser(APIView):
    '''View that updates a info of given user through post request.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        if details.objects.filter(email=data["email"], password=data["password"]).exists():
            user = details.objects.get(
                email=data["email"], password=data["password"])
            user.name = data["name"]
            user.email = data["email"]
            user.password = data["password"]
            user.house_no = data["house_no"]
            user.society = data["society"]
            user.nearby = data["nearby"]
            user.street = data["street"]
            user.pincode = data["pincode"]
            user.area = data["area"]
            user.city = data["city"]
            user.state = data["state"]
            user.save()
            return Response(status=200)

        else:
            return Response(status=404)

    def get(self, request):
        data = request.data
        if details.objects.filter(email=data["email"], password=data["password"]).exists():
            user = details.objects.get(
                email=data["email"], password=data["password"])
            user_serializer = user_details_serializer(user)
            return Response(user_serializer.data, status=200)


class GetCartInfo(APIView):
    '''View that returns all products in cart for given user, it takes user id as parameter, it 
     accepts post request.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.data
        cart_products = cart.objects.filter(user=data["id"])
        cart_serializer = cart_products_serializer(cart_products, many=True)
        return Response(cart_serializer.data, status=200)

    def post(self, request):
        return Response(status=405)


class AddIntoCart(APIView):
    '''View that adds new product into the cartm it takes user_id(id), product_id, quantity as the parameter,
     it accepts the post request.'''
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        data = request.data
        user = details.objects.get(id=data["id"])
        product = product_details.objects.get(id=data["product_id"])
        cart_product = cart.objects.create(
            user=user, product_details=product, quantity=data["quantity"])
        cart_product.save()
        return Response(status=201)

    def get(self, request):
        return Response(status=405)


class DeleteFromCart(APIView):
    '''View that deletes product not quantity from the cart, it takes cart_id as parameter, it accepts 
     post request.'''
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self, request):
        data = request.data
        if cart.objects.filter(id=data["cart_id"]).exists():
            cart_obj = cart.objects.get(id=data["cart_id"])
            cart_obj.delete()
            return Response(status=202)
        return Response(status=404)

    def get(self, request):
        return Response(status=405)


class GetOrderInfo(APIView):
    '''View that returns all info of the given order for given user, it takes uder_id(id) as parameter, 
     it accepts get request.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.data
        user = details.objects.get(id=data["id"])
        if orders.objects.filter(user=user).exists():
            order = orders.objects.filter(user=user)
            order_ser = order_serializer(order, many=True)
            return Response(order_ser.data, status=200)
        return Response(status=404)

    def post(self, request):
        return Response(status=405)


class PlaceOrder(APIView):
    '''View that places and finalizes order, it takes user_id(id), product_id, retailer_id as parameter,
     it accepts post request.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = details.objects.get(id=data["id"])
        product = product_details.objects.get(id=data["product_id"])
        retailer = retailer_details.objects.get(id=data["retailer_id"])

        if product_sold.objects.filter(retailer=data["retailer_id"], product=data["product_id"]).exists():
            product_sold_prev = product_sold.objects.get(
                retailer=data["retailer_id"])
            product_sold_prev.product_pieces = int(
                product_sold_prev.product_pieces)+1
            product_sold_prev.save()
        else:
            product_sold_obj = product_sold.objects.create(
                retailer=retailer, product=product, product_pieces="1")
            product_sold_obj.save()
        order = orders.objects.create(user=user, product_details=product)
        order.save()

        return Response(status=201)

    def get(self, request):
        return Response(status=405)


class CancelOrder(APIView):
    '''View that cancels the given order for given user, it takes order_id,retailer_id,product_id as parameters,
    it accepts get request.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        if orders.objects.filter(id=data["order_id"]).exists():
            if product_sold.objects.filter(retailer=data["retailer_id"], product=data["product_id"]).exists():
                product_sold_prev = product_sold.objects.get(
                    retailer=data["retailer_id"])
                product_sold_prev.product_pieces = int(
                    product_sold_prev.product_pieces)-1
                product_sold_prev.save()
            else:
                return Response(status=404)
            order = orders.objects.get(id=data["order_id"])
            order.delete()
            return Response(status=202)
        return Response(status=404)

    def get(self, request):
        return Response(status=405)


class LoginUser(APIView):
    '''View that logs user in and it takes email and password of the user and returns the token.
     it accepts the post request.'''
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login_log_obj = login_log(user=user)
        login_log_obj.save()
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"key": str(token)})

    def get(self, request):
        return Response(status=405)


class LogoutUSer(APIView):
    '''View that logs out the user. it takes token, it accepts post request.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        django_logout(request)
        return Response(status=200)

    def get(self, request):
        return Response(status=405)


class IncrementProductInCart(APIView):
    '''View that increment the quantity of the product in the cart. it takes cart_id as parameter,
    it accepts post request.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        cart_obj = cart.objects.get(id=data["cart_id"])
        cart_obj.quantity = int(cart_obj.quantity)+1
        cart_obj.save()
        return Response(status=200)

    def get(self, request):
        return Response(status=405)


class DecrementProductInCart(APIView):
    '''View that decrements the quantity of the cart product, it takes cart_id as parameter, it accepts
     post request.'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        cart_obj = cart.objects.get(id=data["cart_id"])
        if int(cart_obj.quantity) > 1:
            cart_obj.quantity = int(cart_obj.quantity)-1
            cart_obj.save()
            return Response(status=200)
        cart_obj.delete()
        return Response(status=200)

    def get(self, request):
        return Response(status=405)

