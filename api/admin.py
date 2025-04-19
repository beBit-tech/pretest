from django.contrib import admin
from .models import Order

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'total_price', 'created_time')
    search_fields = ('order_number', )
    list_filter = ('created_time', )
