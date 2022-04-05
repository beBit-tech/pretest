from django.db import models

class Product(models.Model):
    product_number = models.PositiveIntegerField()
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15, decimal_places=2)

class Order(models.Model):
    order_number = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)