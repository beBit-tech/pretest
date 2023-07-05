from django.contrib import admin
from django.urls import path
from api.views import import_order, create_product, delete_products, update_products

urlpatterns = [
    path('import-order/', import_order, name='import_order'),
    path('products/create/', create_product),
    path('products/delete/', delete_products),
    path('products/update/', update_products),
]