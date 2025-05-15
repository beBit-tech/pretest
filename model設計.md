

### BuyUser

name:用戶名稱
age:
email:

### order
    應該只會出自對同一個賣家中商場中的商品作評價
- order_num : 訂單編號
- total_price: 總金額  // 統計所有購買商品的總金額
- created: 訂單成立時間

Foreignkey: 
- buyer: 一個買家可能擁有多筆訂單

### Product cell
    多種不同的商品可能來自同一個 order 之中
    這項商品的出售來自的細節項目

- sell_null: 售出數量

**one to one**
- product: 銷售出去的產品細節

**ForeignKey**
- from_order 





### Product

    賣家陳列商品的: 品項名稱、單一價格、庫存數量、商品描述


- name: 商品名稱
- stack:庫存
- price: 售價
- descript: 商品描述

ForeignKey:
- seller: 賣家  # 一個賣家會賣多種不同的商品



### Comments 評論
'''
一個訂單(唯一性) 一則購買他的留言  (1 to 1)
一個人可以擁有多條留言、但一條留言只會是由一個人所撰寫的 (F)
'''
- content
- created

OnetoOneField:
- order

ForeignKey:
- buyer



### Seller

買家可同時是賣家
OnetoOneField:
- buyer


多個買家會擁有多個通路(賣家這邊做選擇)
ManytoManyField:
- pathway


