from django.db import models
import uuid

# Create your models here

class Order(models.Model):
    # order model
    Order_number = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Total_price = models.FloatField()
    Created_time = models.DateTimeField(auto_now_add=True)
    Detail = models.TextField(max_length=200)
    products = models.ManyToManyField(to='Product')

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.Order_number}'

class Product(models.Model):
    # product model
    Product_name = models.TextField(max_length=200)
    Product_price = models.FloatField()
    Product_genre = models.TextField(max_length=200)

    def __str__(self):
        return self.Product_name

