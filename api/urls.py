from api.views import import_order
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('import-order/', import_order)
]