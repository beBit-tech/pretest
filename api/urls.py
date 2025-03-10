from django.contrib import admin
from django.urls import path
from api.views import import_order

urlpatterns = [
    path("import_order/", import_order)
]