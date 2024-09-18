import uuid
from django.db import models


# Order Model
class Order(models.Model):
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_time = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField('Product', through='OrderItem')

    def calculate_total_price(self):
        total = sum(item.unit_price * item.quantity for item in self.orderitem_set.all())
        self.total_price = total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_total_price()

    def __str__(self):
        return f"{self.order_number}"

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

# OrderItem Model (Intermediate Model)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)
        self.order.calculate_total_price()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.order.order_number}"