from django.urls import path
from .views import SignUpRetailer
urlpatterns = [
    path('api/create-retailer/', SignUpRetailer.as_view()),
  
]
