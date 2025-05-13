# 訂單管理系統 API 修改說明

## 主要功能改進

### 1. 資料模型強化 (models.py)
- 建立三表關聯結構：Order(訂單)、Product(商品)、OrderItem(訂單明細)
- 自動化總價計算邏輯：
```python
  def save(self, *args, **kwargs):
      self.order.total_price = sum(item.product.price * item.quantity 
                                 for item in self.order.orderitem_set.all())
```
- 加入價格範圍驗證機制 (0 < price < 1,000,000,000)

### 2. 訂單處理邏輯(views.py)
```python
@api_view(['POST'])
@token_required
def import_order(request):
    # 事務處理確保資料原子性
    with transaction.atomic():
        # 多層次驗證機制：
        # 1. 輸入格式檢查
        # 2. UUID 合法性驗證
        # 3. 商品存在性確認
        # 4. 數量有效性檢查
        
        # 錯誤處理流程：
        if errors:
            transaction.set_rollback(True)
            return Response({'errors': errors}, 400)
```

### 3. 測試案例強化 (tests.py)
```python
- 授權驗證測試(缺少token、無效token)
- 商品數據結構驗證測試(空商品、非陣列儲存Product)
- 商品項目驗證測試(不存在的商品、無ID)
- 數量驗證測試(商品數量為0)
```

## API 測試指令

### POST 方法測試 (Port 8008)
```bash
curl -X POST http://localhost:8008/api/import-order/ \
  -H "Content-Type: application/json" \
  -d '{
	"access_token":"omni_pretest_token",
    "products": [
      {"product_id": "095fbbf0-e34a-4ba1-8112-e68455b7eb18", "quantity": 1},
      {"product_id": "01fe9fe6-4054-4776-90f0-76bed0053ad2", "quantity": 2},
      {"product_id": "584b7428-eb51-4a0e-8c8b-6427fb3f7882", "quantity": 1}
    ]
  }'
```

### Django Admin(for test)
```bash
Account:root
Password:12345678
```
## 商品清單範例

| 商品UID                                | 商品名稱   | 價格    |
| ------------------------------------ | ------ | ----- |
| 095fbbf0-e34a-4ba1-8112-e68455b7eb18 | 智慧手環   | 899   |
| 01fe9fe6-4054-4776-90f0-76bed0053ad2 | 無線藍牙耳機 | 1299  |
| 584b7428-eb51-4a0e-8c8b-6427fb3f7882 | 筆記型電腦  | 30000 |

