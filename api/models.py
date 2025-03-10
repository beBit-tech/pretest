import uuid
from django.db import models
from django.core.exceptions import ValidationError


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
        """
        Create an order with the given total price and product IDs.
        Raises a ValidationError if any of the product IDs are invalid or 
        the total price does not match the sum of the product prices.

        :param total_price: The total price of the order
        :param product_ids: A list of product IDs
        :return: The created order
        """
        products = []
        invalid_product_ids = []
        for product_id in product_ids:
            try:
                products.append(Product.objects.get(product_id=product_id))
            except Product.DoesNotExist:
                invalid_product_ids.append(product_id)

        if invalid_product_ids:
            raise ValidationError('Invalid product IDs: {}'.format(', '.join(invalid_product_ids)))
        
        if sum(product.price for product in products) != total_price:
            raise ValidationError('Total price does not match the sum of product prices')

        order = cls.objects.create(total_price=total_price)
        order.products.set(products)
        order.save()
        return order