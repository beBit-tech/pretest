from django.db import models
from datetime import datetime
import shortuuid

class ProductType(models.IntegerChoices):
    TYPE_A = 1, 'type_a'
    TYPE_B = 2, 'type_b'
    TYPE_C = 3, 'type_c'


class ProductMaterial(models.IntegerChoices):
    METAL = 1, 'metal'
    CLOTH = 2, 'cloth'
    WOOD = 3, 'wood'


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=20, unique=True, default='')
    total_price = models.DecimalField(decimal_places=2, max_digits=7)
    product_id = models.CharField(max_length=8)
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.order_number == '':
            self.order_number = f'ON' + datetime.now().strftime('%Y%d%m%H%M%S')
        super().save(*args, **kwargs)


class Product(models.Model):
    id = models.CharField(max_length=8, primary_key=True, default='')
    type = models.IntegerField(choices=ProductType.choices)
    material = models.IntegerField(choices=ProductMaterial.choices)

    def save(self, *args, **kwargs):
        if self.id == '':
            self.id = shortuuid.uuid()[:8]
        super().save(*args, **kwargs)
