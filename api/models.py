from django.db import models
from datetime import datetime


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=20, unique=True, default='')
    total_price = models.DecimalField(decimal_places=2, max_digits=7)
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.order_number == '':
            self.order_number = f'ON' + datetime.now().strftime('%Y%d%m%H%M%S')
        super().save(*args, **kwargs)

