from django.db import models

class Order(models.Model):
    Order_number = models.CharField(max_length=20, unique=True)
    Total_price = models.DecimalField(max_digits=10, decimal_places=2)
    Created_time = models.DateTimeField(auto_now_add=True)
    Customer_name = models.CharField(max_length=100, null=True, blank=True)
    Status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Shipped", "Shipped"), ("Delivered", "Delivered")],
        default="Pending"
    )
    
    def __str__(self):
        return f"Order {self.Order_number} - {self.Total_price} ({self.Status})"
    pass

