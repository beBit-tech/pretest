from django.db import models
# __str__ 4 better presentation

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(default=0)  # amount in stock
    def __str__(self):
        return self.name

class Order(models.Model):
    order_number = models.CharField(max_length=255, unique=True)
    total_price = models.PositiveIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through="ProductOrder")

    def __str__(self):
        return self.order_number

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order.order_number} - {self.product.name} ({self.quantity})"

