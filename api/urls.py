from django.urls import path
from api.views import (
    import_order, create_product, 
    delete_product, list_orders, 
    get_order_by_number, get_order_by_product,
    update_product, delete_order
)

urlpatterns = [
    path("import-order/", import_order),
    path("create-product/", create_product),
    path("delete-product/<uuid:product_number>/", delete_product),
    path("update-product/<uuid:product_number>/", update_product),
    path("list-orders/", list_orders),
    path("get-order-by-number/<uuid:order_number>/", get_order_by_number),
    path("get-order-by-product/<uuid:product_number>/", get_order_by_product),
    path("delete-order/<uuid:order_number>/", delete_order),
]