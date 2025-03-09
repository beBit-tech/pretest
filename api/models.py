from django.db import models


# Create your models here.
class Product(models.Model):
    product_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    @classmethod
    def generate_product_id(cls):
        last_product = cls.objects.last()
        if last_product:
            return str(int(last_product.product_id) + 1)
        return '1'
    
    @classmethod
    def create_product(cls, name, price):
        product_id = cls.generate_product_id()
        return cls.objects.create(product_id=product_id, name=name, price=price)


class Order(models.Model):
    order_number = models.CharField(max_length=100, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self):
        return self.order_number

    @classmethod
    def generate_order_number(cls):
        last_order = cls.objects.last()
        if last_order:
            return str(int(last_order.order_number) + 1)
        return '1'
    
    @classmethod
    def create_order(cls, total_price, product_ids):
        order_number = cls.generate_order_number()
        products = Product.objects.filter(id__in=product_ids)
        order = cls.objects.create(order_number=order_number, total_price=total_price)
        order.products.set(products)
        return order