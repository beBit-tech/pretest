from django.db import models
from django.core.validators import MinValueValidator


class Order(models.Model):
    order_number = models.AutoField(primary_key=True, help_text="訂單編號")
    total_price = models.IntegerField(validators=[MinValueValidator(1)], help_text="總金額")
    created_time = models.DateTimeField(auto_now_add=True, help_text="訂單建立時間")
    products = models.ManyToManyField("Product", through="OrderProduct", help_text="商品")


class Product(models.Model):
    name = models.CharField(max_length=50, help_text="商品名稱")
    price = models.IntegerField(validators=[MinValueValidator(1)], help_text="商品價格")
    detail = models.TextField(null=True, help_text="商品描述")
    status = models.BooleanField(default=False, help_text="是否上架")
    amount = models.IntegerField(validators=[MinValueValidator(0)], help_text="商品數量")
    updated_time = models.DateTimeField(auto_now=True, help_text="商品資料更新時間")
    created_time = models.DateTimeField(auto_now_add=True, help_text="商品建立時間")


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, help_text="訂單")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, help_text="商品")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], help_text="數量")
