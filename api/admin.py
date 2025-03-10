from django.contrib import admin
from api.models import Order
# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'total_price', 'created_time')
    search_fields = ('order_number',)
    ordering = ('-created_time',)
