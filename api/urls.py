from django.urls import path
from api.views import import_order, list_orders

urlpatterns = [
    path('import_order/', import_order),
    path('orders/', list_orders),
]