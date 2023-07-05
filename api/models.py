from django.db import models


PRODUCT_STATUS_CHOICES = [
    ('available', 'Available'),
    ('out_of_stock', 'Out of Stock'),
    ('discontinued', 'Discontinued'),
]

DELIVERY_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('delivered', 'Delivered'),
]

PAYMENT_METHOD_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('paypal', 'PayPal'),
    ('bank_transfer', 'Bank Transfer'),
    ('cash_on_delivery', 'Cash on Delivery'),
]

class Product(models.Model):
    product_number = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=200, choices=PRODUCT_STATUS_CHOICES, default='available')


class Order(models.Model):
    order_number = models.AutoField(primary_key=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)
    deliver_status = models.CharField(max_length=200, choices=DELIVERY_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=200, choices=PAYMENT_METHOD_CHOICES, default='cash_on_delivery')
    products = models.ManyToManyField(Product, through='OrderProduct')


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = (('product', 'order'),)
