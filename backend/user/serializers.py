from django.db.models import fields
from rest_framework import serializers
from .models import details,cart,orders
from rest_framework import exceptions
from django.contrib.auth import authenticate

class user_details_serializer(serializers.ModelSerializer):
    class Meta:
        model=details
        fields='__all__'

class cart_products_serializer(serializers.ModelSerializer):
    class Meta:
        model=cart
        fields='__all__'

class order_serializer(serializers.ModelSerializer):
    class Meta:
        model=orders
        fields='__all__'

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self,data):
        email=data["email"]
        password=data["password"]
        if email and password:
            user=authenticate(email=email,password=password)
            print(user)
            if user:
                if user.is_active:
                    data["user"]=user
                else:
                    msg="User Account Is Deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                msg="Username or Password is incorrect"
                raise exceptions.ValidationError(msg)
        else:
            msg="Credentials were not provided"
            raise exceptions.ValidationError(msg)
        return data