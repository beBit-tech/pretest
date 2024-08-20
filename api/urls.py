from django.contrib import admin
from django.urls import path

from api.views import (
    create_customer,
    create_product,
    get_orders_by_customer,
    get_products,
    import_order,
)

urlpatterns = [
    path("import-order/", import_order, name="import_order"),
    path("create-customer/", create_customer, name="create_customer"),
    path("create-product/", create_product, name="create_product"),
    path("get-products/", get_products, name="get_products"),
    path(
        "get-orders-by-customer/<str:username>/",
        get_orders_by_customer,
        name="get_orders_by_customer",
    ),
]
