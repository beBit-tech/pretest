from django.db import models
import uuid
from decimal import Decimal
from django.core.validators import MinValueValidator

class Order(models.Model):
    order_number = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    total_price = models.DecimalField(max_digits=12,decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    quantity=models.PositiveIntegerField()
    buyer = models.CharField(max_length=64,blank=False,null=False)
    created_time = models.DateTimeField(auto_now_add=True)
    last_update=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"buyer {self.buyer}, Order Number :{self.order_number}.Created : {self.created_time}, last update : {self.last_update}"    

class Product(models.Model):
    product_number = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=12,decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    quantity=models.PositiveIntegerField()
    status=models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} : ${self.price}, Quantity:{self.quantity}"

class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orders")
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Product:{self.product} {self.quantity}"
