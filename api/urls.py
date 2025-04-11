from django.contrib import admin
from django.urls import path
from api.views import import_order, add_product, add_customer, get_order_detail, get_customer_orders, delete_orders

urlpatterns = [
    path('import-order/', import_order, name='import_order'),
    path('add-product/', add_product, name='add_product'),
    path('add-customer/', add_customer, name='add_customer'),
    path('get-order/<str:order_number>/', get_order_detail, name='get_order_detail'),
    path('customer-order/<str:customer_uid>/', get_customer_orders, name='get_customer_order'),
    path('delete-order/', delete_orders, name='delete_order'),
]