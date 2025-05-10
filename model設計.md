

### BuyUser

name:用戶名稱
age:
email:

### order
- order_num : 訂單編號
- total_price: 總金額
- created: 訂單成立時間

Foreignkey: 
- buyer: 一個買家可能擁有多筆訂單



### Product
商品陳列
- name: 商品名稱
- stack:庫存
- price: 售價
- descript: 商品描述

ForeignKey:
- seller: 賣家  # 一個賣家會賣多種不同的商品

ManytoMany:


### ProductSeller

- sell_num: 銷量
OnetoOneField:
- product: 一項商品對應相對應的商品

ForeignKey:
- order: 多個商品銷售可能對應到同一筆訂單



### Comments 評論
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


### Pathway
- name: 通路名稱
- price: 運費



