from django.urls import path
from .views import AddNewProduct,DeleteProduct,GetProductsByRetailerId,GetProductsBySearch,GetOrderInvoice,DefaultHomeProducts,DefaultHomeCatagory,AllCatagories

urlpatterns = [
    path('api/add-new-product/', AddNewProduct.as_view()),
    path('api/delete-product/', DeleteProduct.as_view()),
    path('api/get-product-by-retailer-id/', GetProductsByRetailerId.as_view()),
    path('api/get-product-by-search/', GetProductsBySearch.as_view()),
    path('api/get-order-invoice/', GetOrderInvoice.as_view()),
    path('api/default-home-products/', DefaultHomeProducts.as_view()),
    path('api/default-home-catagories/', DefaultHomeCatagory.as_view()),
    path('api/all-catagories/', AllCatagories.as_view()),

]
