from django.db import models
from django.utils import timezone
import uuid
import random
import string

# Create your models here.

# 產品模型
class Product(models.Model):
    uid = models.CharField(max_length=6, unique=True, blank=True) # 商品uid
    name = models.CharField(max_length=100) # 商品名稱
    price = models.DecimalField(max_digits=10, decimal_places=2) #商品價格

    def save(self, *args, **kwargs):
        if not self.uid:
            last_product = Product.objects.last()
            if last_product:
                last_number = int(last_product.uid[1:])
                new_uid = f"P{str(last_number + 1).zfill(5)}"
            else:
                new_uid = "P00001"
            self.uid = new_uid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.uid

class Customer(models.Model):
    uid = models.CharField(max_length=6, unique=True, blank=True) # 顧客uid
    name = models.CharField(max_length=100) # 顧客姓名

    def save(self, *args, **kwargs):
        if not self.uid:
            last_customer = Customer.objects.last()
            if last_customer:
                last_number = int(last_customer.uid[1:])
                new_uid = f"C{str(last_number + 1).zfill(5)}"
            else:
                new_uid = "C00001"
            self.uid = new_uid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.uid

class Order(models.Model):
    # Add your model here
    order_number = models.CharField(max_length=32, unique=True) # 訂單編號
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) # 訂單建立者
    total_price = models.DecimalField(max_digits=10, decimal_places=2) # 訂單總價
    created_time = models.DateTimeField(default=timezone.now) # 訂單建立時間

    def save(self, *args, **kwargs):
        if not self.order_number:
            timestamp = self.created_time.strftime('%Y%m%d%H%M%S')
            random_code = ''.join(random.choices(string.digits, k=9))  # 9 碼數字
            self.order_number = f"ORD{timestamp}{self.customer.uid}{random_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number}"

class OrderProduct(models.Model):
    # 紀錄訂單中的產品數量
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order', 'product')  # 確保每筆訂單中相同產品只能出現一次

    def __str__(self):
        return f"Order {self.order.order_number} - Product {self.product.uid} - Quantity {self.count}"
