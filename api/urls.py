from django.contrib import admin
from django.urls import path
from .views import import_order, orderList, orderDetail, orderUpdate, orderDelete


urlpatterns = [
    path('import-order/', import_order),
    path('order-list/', orderList),
    path('order-detail/<str:pk>/',orderDetail),
    path('order-update/<str:pk>/', orderUpdate),
    path('order-delete/<str:pk>/', orderDelete)
]