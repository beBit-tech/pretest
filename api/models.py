from django.db import models


# Create your models here.
class Order(models.Model):
    # Add your model here
    order_number = models.IntegerField(unique=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order #{self.order_number} - ${self.total_price} ({self.created_time.strftime('%Y-%m-%d %H:%M')})"
