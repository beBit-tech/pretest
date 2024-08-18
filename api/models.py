from django.db import models


# Create your models here.
class Order(models.Model):
    order_number = models.CharField(max_length=63, unique=True)
    total_price  = models.PositiveIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

