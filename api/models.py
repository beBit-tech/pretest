from django.db import models



class Order(models.Model):
    order_number = models.BigAutoField(auto_created=True,primary_key=True)
    total_price = models.IntegerField(null=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order<{self.order_number} with price {self.total_price}>'

