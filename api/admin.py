from django.contrib import admin
from .models import Order,BuyUser, Pathway, Product,Comment,Seller,ProductSell
# Register your models here.



# admin.site.register(BuyUser)
# admin.site.register(Order)
admin.site.register(BuyUser)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','order_num')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','seller')


@admin.register(ProductSell)
class ProductSellAdmin(admin.ModelAdmin):
    list_display = ('id','get_seller_name','get_product_name')

    def get_seller_name(self, obj):
        """獲取關聯 BuyUser 的 name 屬性。"""
        if obj.product.seller:
            return obj.product.seller.buyeruser.name
        return None

    get_seller_name.short_description = "賣家名稱"
    
    def get_product_name(self,obj):
        if obj.product:
            return obj.product.name
        return None
    
    get_product_name.short_description = "商品名"



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','__str__','get_buyer_name','create_time')


    def get_buyer_name(self, obj):
        """獲取關聯 BuyUser 的 name 屬性。"""
        if obj.buyuser:
            return obj.buyuser.name
        return None



admin.site.register(Seller)
admin.site.register(Pathway)




