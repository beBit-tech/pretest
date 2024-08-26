from django.db import models


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(default = 0) #amount on stock


class Order(models.Model):
    order_number = models.CharField(max_length=255, unique=True)
    total_price = models.PositiveIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="ProductOrder")

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)


