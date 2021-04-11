from django.urls import path
from .views import DecrementProductInCart, PlaceOrder, SignUpUser,DeleteUser,UpdateInfoUser,GetCartInfo,AddIntoCart,DeleteFromCart,PlaceOrder,CancelOrder,GetOrderInfo,LoginUser,LogoutUSer,IncrementProductInCart,DecrementProductInCart


urlpatterns = [
    path('api/create-user/', SignUpUser.as_view()),
    path('api/delete-user/', DeleteUser.as_view()),
    path('api/update-user/', UpdateInfoUser.as_view()),
    path('api/get-cart/', GetCartInfo.as_view()),
    path('api/add-cart/', AddIntoCart.as_view()),
    path('api/delete-cart/', DeleteFromCart.as_view()),
    path('api/place-order/', PlaceOrder.as_view()),
    path('api/cancel-order/', CancelOrder.as_view()),
    path('api/get-order/', GetOrderInfo.as_view()),
    path('api/login-user/', LoginUser.as_view()),
    path('api/logout-user/', LogoutUSer.as_view()),
    path('api/increment-cart-product/', IncrementProductInCart.as_view()),
    path('api/decrement-cart-product/', DecrementProductInCart.as_view()),
]
