from django.db import models


# Create your models here.
class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_id + ' - ' + self.name
    
    @classmethod
    def create_product(cls, name, price):
        """
        Create a product with the given name and price.
        
        :param name: The name of the product
        :param price: The price of the product
        :return: The created product
        """
        return cls.objects.create(name=name, price=price)


class Order(models.Model):
    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, related_name='orders')

    def __str__(self):
        return self.order_number

    @classmethod
    def create_order(cls, total_price, product_ids):
        order_number = cls.generate_order_number()
        products = Product.objects.filter(id__in=product_ids)
        order = cls.objects.create(order_number=order_number, total_price=total_price)
        order.products.set(products)
        return order