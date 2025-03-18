from django.contrib import admin
from .models import Order, Product, OrderProduct

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'total_price', 'created_time')  # 在 Django Admin 介面顯示這些欄位
    search_fields = ('order_number',)

# Product 管理介面
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'created_time')
    search_fields = ('product_id',)


# OrderProduct 管理介面
@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_at_order_time')
    search_fields = ('order__order_number', 'product__name')