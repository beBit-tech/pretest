from django.db import models
from django.utils import timezone

# Create your models here.
class Order(models.Model):
    # Add your model here
    order_number = models.CharField(max_length=100, unique=True) # 訂單編號
    total_price = models.DecimalField(max_digits=10, decimal_places=2) # 訂單總價
    created_time = models.DateTimeField(default=timezone.now) # 訂單建立時間

    def __str__(self):
        return f"Order {self.order_number}"

