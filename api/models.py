from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(blank = True, null = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    stock = models.PositiveIntegerField(default = 0)
    created_time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name

class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    order_number = models.CharField(max_length = 255, unique = True)
    total_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    customer_name = models.CharField(max_length = 255, default = "Unknown")
    customer_email = models.EmailField(default = "unknown@example.com")
    created_time = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = "pending")

    products = models.ManyToManyField(Product, related_name = "orders")

    def __str__(self):
        return f"Order {self.order_number} - ${self.total_price}"
    
