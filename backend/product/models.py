from django.db import models

# Create your models here.
class catagory(models.Model):
    name=models.CharField(max_length=30,null=False)

class details(models.Model):
    product_catagory=models.ForeignKey(catagory,on_delete=models.DO_NOTHING)
    name=models.CharField(max_length=200,null=False)
    img_name=models.CharField(max_length=250,null=False)
    video_name=models.CharField(max_length=250,null=False)
    price=models.CharField(max_length=6,null=False)
    description1=models.CharField(max_length=2000,null=False)
    description2=models.CharField(max_length=2000,null=False)
    description3=models.CharField(max_length=2000,null=False)
    avg_star_rating=models.CharField(max_length=3,default=0)
    retailer_details=models.ForeignKey('retailer.details',on_delete=models.DO_NOTHING)

class review(models.Model):
    user=models.ForeignKey('user.details',on_delete=models.CASCADE)
    description=models.CharField(max_length=300,null=False)
    star=models.CharField(max_length=1,default=0)
    product=models.ForeignKey(details,on_delete=models.CASCADE)
