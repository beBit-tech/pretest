from django.contrib import admin
from django.urls import path

from api import views


urlpatterns = [
    path('', views.api_root),
    path('import-order/', views.import_order, name='import-order')
]