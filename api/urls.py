from django.contrib import admin
from django.urls import path
from api.views import import_order

urlpatterns = [
    # This line was 'import-order', but other else is 'import_order' , i think this is cofusing, so i changed it to underscore.
    path('import_order/', import_order)
]