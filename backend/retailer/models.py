from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class details(models.Model):
    shop_name=models.CharField(max_length=20,null=False)
    email=models.EmailField(max_length=50,null=False,unique=True)
    password=models.CharField(max_length=30,null=False)
    phone_number=models.CharField(max_length=10,null=False,unique=True)
    shop_no=models.CharField(max_length=10,null=False)
    society=models.CharField(max_length=20,null=False)
    nearby=models.CharField(max_length=20,null=False)
    street=models.CharField(max_length=20,null=False)
    pincode=models.CharField(max_length=6,null=False)
    area=models.CharField(max_length=20,null=False)
    city=models.CharField(max_length=20,null=False)
    state=models.CharField(max_length=20,null=False)



class login_log(models.Model):
    retailer=models.ForeignKey(details,on_delete=models.DO_NOTHING)
    time_stamp=models.DateTimeField(auto_now_add=True)

class product_sold(models.Model):
    retailer=models.ForeignKey(details,on_delete=models.CASCADE)
    product=models.ForeignKey('product.details',on_delete=models.DO_NOTHING)
    product_pieces=models.CharField(max_length=5,default=0)

class deleted_accounts(models.Model):
    shop_name=models.CharField(max_length=20,null=False)
    email=models.EmailField(max_length=50,null=False,unique=True)
    password=models.CharField(max_length=30,null=False)
    phone_number=models.CharField(max_length=10,null=False,unique=True)
    shop_no=models.CharField(max_length=10,null=False)
    society=models.CharField(max_length=20,null=False)
    nearby=models.CharField(max_length=20,null=False)
    street=models.CharField(max_length=20,null=False)
    pincode=models.CharField(max_length=6,null=False)
    area=models.CharField(max_length=20,null=False)
    city=models.CharField(max_length=20,null=False)
    state=models.CharField(max_length=20,null=False)
    time_stamp=models.DateTimeField(auto_now_add=True)
