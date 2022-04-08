from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import (
    orders_detail,orders_list,import_order,
    products_detail,products_list,import_product,)

schema_view = get_schema_view(
   openapi.Info(
      title="Pretest API",
      default_version='v1',
      description="with Model Order and Product",
      contact=openapi.Contact(email="yeh.mentos@gmail.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('orders',orders_list,name='orders-list'),
    path('orders/<uuid:pk>',orders_detail,name='orders-detail'),
    path('orders/import-order',import_order,name='import-order'),
    path('products',products_list,name='products-list'),
    path('products/<uuid:pk>',products_detail,name='products-detail'),
    path('products/import-product',import_product,name='import-product'),    
]