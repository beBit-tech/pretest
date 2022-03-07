from django.contrib import admin
from .models import Order
from .models import Product

# Define the Orderadmin class
class OrderAdmin(admin.ModelAdmin):
    list_display = ('Order_number', 'Total_price', 'Detail', 'Created_time')

# Register the admin class with the associated model
admin.site.register(Order, OrderAdmin)

# Define the Productadmin class
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Product_name', 'Product_price', 'Product_genre')

admin.site.register(Product, ProductAdmin)
