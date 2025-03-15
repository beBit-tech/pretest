from api.views import create_or_update_product, delete_product, get_order_details, import_order
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('import-order/', import_order),
    path('create-or-update-product/', create_or_update_product),
    path('delete-product/', delete_product),
    path('order/<str:order_number>/', get_order_details)
]
