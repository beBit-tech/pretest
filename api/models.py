from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

def validate_price(value):
    if value < 0 or value >= 1000000000:
        raise ValidationError("總金額需大於0或小於1000000000")
    else:
        return value
    
class Order(models.Model):
    order_number = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="訂單編號"
    )

    products = models.ManyToManyField(
        'Product',
        through='OrderItem',
        verbose_name="購買商品"
    )

    total_price = models.PositiveIntegerField(
        default=0,
        verbose_name="總金額",
        validators=[validate_price]
    )

    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="建立時間"
    )

    def __str__(self):
        return f"{self.order_number}"

    class Meta:
        verbose_name = "訂單"
        verbose_name_plural = "訂單"
        ordering = ['-created_time']

class Product(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="商品UID"
    )
    name = models.CharField(max_length=255, verbose_name="商品名稱")
    price = models.PositiveIntegerField(
        validators=[validate_price],
        verbose_name="商品價格"
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    def __str__(self):
        return f"{self.uid} - {self.name} - {self.price}"

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"
        ordering = ['-created_time']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="所屬訂單")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品")
    quantity = models.PositiveIntegerField(default=1, verbose_name="購買數量")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 更新訂單總金額
        self.order.total_price = sum(item.product.price * item.quantity for item in self.order.orderitem_set.all())
        self.order.save()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        # 更新訂單總金額
        self.order.total_price = sum(item.product.price * item.quantity for item in self.order.orderitem_set.all())
        self.order.save()

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    class Meta:
        verbose_name = "訂單明細"
        verbose_name_plural = "訂單明細"
        unique_together = ('order', 'product')
