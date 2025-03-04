from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} - ${self.price}"


class Order(models.Model):
    order_number = models.IntegerField(unique=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    created_time = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(
        Product, through="OrderItem", related_name="orders"
    )

    def __str__(self) -> str:
        return f"Order #{self.order_number} - ${self.total_price} ({self.created_time.strftime('%Y-%m-%d %H:%M')})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self) -> str:
        return (
            f"{self.product.name} x {self.quantity} in Order #{self.order.order_number}"
        )

    @property
    def sub_total(self) -> float:
        return self.quantity * float(self.unit_price)
