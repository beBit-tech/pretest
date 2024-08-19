from django.db import models

# Create your models here.


class Customer(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=0)


class Order(models.Model):
    order_number = models.CharField(max_length=63, unique=True)
    total_price = models.PositiveIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    # Relationship with Product
    products = models.ManyToManyField(
        Product, through="OrderProduct", related_name="orders"
    )

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
