from django.contrib import admin
from django.urls import path

from .views_order import import_order, order_detail
from .views_product import create_product, delete_product

urlpatterns = [
    path('import-order/', import_order, name='import-order'),
    path("create-product/", create_product, name="create-product"),
    path('delete-product/', delete_product, name='delete-product'),
    path("order-detail/<str:order_number>/", order_detail, name="order-detail"),
]