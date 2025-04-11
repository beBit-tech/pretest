from django.contrib import admin
from django.urls import path
from api.views import import_order, add_product, add_customer

urlpatterns = [
    path('import-order/', import_order, name='import_order'),
    path('add-product/', add_product, name='add_product'),
    path('add-customer/', add_customer, name='add_customer')
]