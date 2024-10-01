from django.contrib import admin
from django.urls import path
from api.adapter.controller.order.order_views import import_order
from api.adapter.controller.product.product_views import create_product
from api.adapter.controller.product.product_views import get_all_products

urlpatterns = [
    path('import-order/', import_order, name = "import_order"),
    path('product/', create_product, name = "create_product"),
    path('products/', get_all_products, name = "get_all_products")
]