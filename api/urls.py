from django.contrib import admin
from django.urls import path

from api.views import create_customer, create_product, import_order

urlpatterns = [
    path("import-order/", import_order, name="import_order"),
    path("create-customer/", create_customer, name="create_customer"),
    path("create-product/", create_product, name="create_product"),
]
