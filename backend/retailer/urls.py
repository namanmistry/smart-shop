from django.urls import path
from .views import SignUpRetailer,LoginRetailer,DeleteRetailer,UpdateInfoRetailer,GetProductSoldInfo,GetOrderDetailsForRetailer
urlpatterns = [
    path('api/create-retailer/', SignUpRetailer.as_view()),
    path('api/delete-retailer/', DeleteRetailer.as_view()),
    path('api/update-retailer/', UpdateInfoRetailer.as_view()),
    path('api/login-retailer/', LoginRetailer.as_view()),
    path('api/get-product-sold/', GetProductSoldInfo.as_view()),
    path('api/get-order-details/', GetOrderDetailsForRetailer.as_view()),
    
  
]
