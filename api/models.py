from itertools import product
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User  # django 內建的 user


class BuyUser(models.Model):

    # 使用者 註冊即買家  拓展原本的使用者
    name = models.CharField(max_length=20,verbose_name='買家名')
    age = models.IntegerField(verbose_name='年齡') 
    email = models.EmailField()

    class Meta:

        db_table = 'buyuser'

        pass

    def __str__(self):
        return self.name

    pass



class Order(models.Model):
    

    order_num = models.IntegerField(default = 0, verbose_name = "訂單編號")
    total_price = models.IntegerField(default=0,verbose_name="總金額")
    created = models.DateTimeField(auto_now_add=True,verbose_name="建立時間")



    buyuser = models.ForeignKey(BuyUser,on_delete=models.CASCADE,related_name='order', null=True)   # 一個 user 會有多筆訂單
    

    class Meta:
        db_table='order'

    def __str__(self):
        return '訂單'+str(self.id)


class Pathway(models.Model):

    # 開放通路
    name = models.CharField(max_length=15, verbose_name='通路名稱')

    class Meta:
        db_table = 'pathway'


    def __str__(self):
        return self.name

class Seller(models.Model):

    # 賣家 對應 出售的產品
    buyeruser = models.OneToOneField(BuyUser,on_delete=models.CASCADE,related_name='seller', null=True, blank=True)

    pathway = models.ManyToManyField(Pathway)

    
    class Meta:
        db_table='seller'


    def __str__(self):
        return self.buyeruser.name

    # pass



class Product(models.Model):
    '''商品陳列、相關資訊'''

    name = models.CharField(max_length=50,verbose_name='商品名稱')
    price = models.IntegerField(verbose_name='售價')
    stack = models.IntegerField(verbose_name='庫存')
    descript = models.CharField(verbose_name='商品描述')
    

    # 一個訂單有多個商品 ， 同一種商品可能被多的訂單 訂購
    seller = models.ForeignKey(Seller,related_name='product',on_delete=models.CASCADE,verbose_name='賣家')   # 多個商品可能由同個賣家提供

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name

class ProductSell(models.Model):
    
    
    # 單一一次銷售對應一個商品項目
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='productSell')
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='productSell')

    sell_num = models.IntegerField(verbose_name='銷量')


    class Meta:
        db_table='productsell'

class Comment(models.Model):
    # 每則評論
    content = models.CharField(max_length=250 ,verbose_name='評價')
    create_time = models.DateTimeField(auto_now=True)
    

    # 這條留言屬於
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name='comments',verbose_name="訂單編號")  # 同個產品 會有多個評論
    buyuser = models.OneToOneField(BuyUser,on_delete=models.CASCADE, related_name='comments', null=True, blank=True,verbose_name='留言的買家')   #  同個人會有多則評論
    

    class Meta:
        db_table='comment'

    def __str__(self):
        return "訂單"+str(self.order.order_num)+"的回覆"
    

