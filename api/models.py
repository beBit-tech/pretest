from enum import Enum

from django.db import models


# Create your models here.
class Status(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(models.Model):
    # Add your model here
    order_number = models.CharField(max_length=20, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=[(tag.value, tag.name) for tag in Status], default=Status.PENDING)

    def __str__(self):
        return f"Order {self.order_number}"


class Product(models.Model):
    product_number = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product {self.product_number}: {self.product_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='ordered_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='orders_containing_product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.order_number}"
