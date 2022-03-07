from django.db import models
import uuid

# Create your models here.
class Order(models.Model):
    # order model
    Order_number = models.UUIDField(primary_key=True, default=uuid.uuid4)
    Total_price = models.IntegerField()
    Created_time = models.DateTimeField(auto_now_add=True)
    Detail = models.TextField(max_length=200)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-Created_time']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.Order_number}'

class Product(models.Model):
    # product model
    Product_name = models.TextField(max_length=200)
    Product_price = models.IntegerField()
    Product_genre = models.TextField(max_length=200)

    class Meta:
        ordering = ['-Product_genre']

    def __str__(self):
        return self.Product_name

