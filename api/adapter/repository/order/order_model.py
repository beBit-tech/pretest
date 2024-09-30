from django.db import models
from api.adapter.repository.product.product_model import Product

class Order(models.Model):
    number = models.CharField(max_length = 100, primary_key = True)
    total_price = models.FloatField()
    created_time = models.DateTimeField()
    products = models.ManyToManyField('Product', through = 'OrderProduct')

class OrderProduct(models.Model):
    order_number = models.ForeignKey(Order, on_delete = models.CASCADE)
    product_number = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order_number', 'product_number')