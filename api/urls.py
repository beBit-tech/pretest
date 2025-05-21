from django.contrib import admin
from django.urls import path
from api.views import *

urlpatterns = [

    path('import-order/', import_order, name='import-order'),
    path('import-order2/', import_order2, name='import-order2'),  # valid token with decorator
    path('order_detail/',order_detail,name='order_detail'),
    path('order_feedback/',order_feedback,name ='order_feedback'),

    path('store/',all_store,name ='all_store'),
    path('store_<str:seller_name>/',all_product_from_seller,name ='all_product_from_seller'),
    
]