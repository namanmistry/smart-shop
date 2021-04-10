from rest_framework import serializers
from .models import details,review,catagory

class product_serializer(serializers.ModelSerializer):
    class Meta:
        model=details
        fields='__all__'

class review_serialzer(serializers.ModelSerializer):
    class Meta:
        model=review
        fields='__all__'

class catagory_serializer(serializers.ModelSerializer):
    class Meta:
        model=catagory
        fields='__all__'