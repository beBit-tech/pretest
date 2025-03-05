from django.urls import path

from api.views import (
    import_order,
    place_order,
    product_list_create,
    product_retrieve_update_delete,
)

urlpatterns = [
    path("import-order/", import_order),
    path("place-order/", place_order),
    path("products/", product_list_create),
    path("products/<int:pk>/", product_retrieve_update_delete),
]
