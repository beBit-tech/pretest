from django.contrib import admin
from django.urls import path
from api.views import import_order, import_order_advanced, create_product

urlpatterns = [
    path('import-order/', import_order),
    path('import-order-advanced/', import_order_advanced),
    path('create-product/', create_product)
]