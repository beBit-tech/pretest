from django.contrib import admin
from django.urls import path
from api.views import import_order
from api.view.order import ImportOrderView

urlpatterns = [
    path('import-order/', import_order, name='import-order'),
    path('import-order-decorator/',ImportOrderView.as_view(), name='import-order2'),   # 使用 apiview 
]