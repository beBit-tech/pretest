from django.db import models
from django.core.validators import MinValueValidator

import uuid

class Product(models.Model):
    product_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(validators=[MinValueValidator(0)]) 
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["title"]
    
# Create your models here.
class Order(models.Model):
    STATUS_PENDING = "P"
    STATUS_COMPLETE = "C"
    STATUS_FAILED = "F"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETE, "Complete"),
        (STATUS_FAILED, "Failed")
    ]
    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(validators=[MinValueValidator(0)]) 
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # related_name is used to access OrderItem objects from Order model
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.FloatField(validators=[MinValueValidator(0)]) 
    product_title = models.CharField(max_length=255)
      
    class Meta:
        unique_together = ["product", "order"]
