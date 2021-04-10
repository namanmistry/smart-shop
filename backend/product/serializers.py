from rest_framework import serializers
from .models import details,review

class product_serializer(serializers.ModelSerializer):
    class Meta:
        model=details
        fields='__all__'

class review_serialzer(serializers.ModelSerializer):
    class Meta:
        model=review
        fields='__all__'

