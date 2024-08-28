from django.urls import path
from .views import import_order, get_product, get_order

urlpatterns = [
    path('import-order/', import_order, name='import_order'),
    path('product/<int:product_id>/', get_product, name='get_product'),
    path('order/<int:order_id>/', get_order, name='get_order'),
]