from django.db.models import fields
from rest_framework import serializers
from .models import details,product_sold

class retailer_details_serializer(serializers.ModelSerializer):
    class Meta:
        model=details
        fields='__all__'
    
class product_sold_serializer(serializers.ModelSerializer):
    class Meta:
        model=product_sold
        fields='__all__'