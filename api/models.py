# api/models.py

from django.db import models

# Create your models here.
class Order(models.Model):
    """
    訂單模型，包含：
    - 訂單號碼（唯一）
    - 總價格
    - 創建時間
    """
    order_number = models.CharField(max_length=20, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number} - ${self.total_price}"


class Product(models.Model):
    """
    產品模型，包含：
    - 產品流水號（唯一）
    - 產品名稱
    - 描述
    - 單價
    - 創建時間
    - 商品數量
    """
    product_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product_id} - {self.name}"


class OrderProduct(models.Model):
    """
    `Order` 與 `Product` 的關聯表，額外儲存：
    - 訂單
    - 產品
    - 數量
    - 下單時的價格
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_orders')
    quantity = models.PositiveIntegerField()
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.order.order_number} - {self.product.name}"
    
class OrderNumberSequence(models.Model):
    """
    儲存每日的訂單流水號計數器。
    e.g. date = "20250317", sequence= 1
    """
    date = models.CharField(max_length=8, unique=True)
    sequence = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.date} - {self.sequence}"

    