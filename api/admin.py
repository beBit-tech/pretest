from django.contrib import admin
from .models import Order
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'total_price', 'created_time')
    search_fields = ('order_number',)
    list_filter = ('created_time',)

admin.site.register(Order)