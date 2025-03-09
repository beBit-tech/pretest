from django.contrib import admin
from django.urls import path
from .views import import_order

urlpatterns = [
    path('import_order/', import_order, name='import_order'),
]