from django.contrib import admin
from django.urls import path
from api.views import import_order, list_order, specific_order

urlpatterns = [
    path('list-order/', list_order ),
    path('list-order/<int:id>', specific_order),
    path('import-order/', import_order)
]