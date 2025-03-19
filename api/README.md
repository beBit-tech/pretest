# Django Omni Pre-Test

此專案以 **Django** + **Django REST framework** 為基礎，實作了一個簡易的訂單管理系統，提供下列功能：

1. 產品管理（新增 / 刪除產品）
2. 訂單匯入（自動產生訂單編號並計算總金額）
3. 查詢訂單細節

## 目錄
1. [專案架構說明](#專案架構說明)
2. [資料庫結構](#資料庫結構)
   - [1. Order](#1-order-訂單表)
   - [2. Product](#2-product-產品表)
   - [3. OrderProduct](#3-orderproduct-訂單與產品關係表)
   - [4. OrderNumberSequence](#4-ordernumbersequence-訂單編號序號表)
3. [API 說明](#api-說明)
   - [1. 建立產品 (POST /api/create-product/)](#1-建立產品-post-apicreate-product)
   - [2. 刪除產品 (DELETE /api/delete-product/)](#2-刪除產品-delete-apidelete-product)
   - [3. 匯入訂單 (POST /api/import-order/)](#3-匯入訂單-post-apiimport-order)
   - [4. 查詢訂單 (GET /api/order-detail/<order_number>/)](#4-查詢訂單-get-apiorder-detailorder_number)
4. [Token 驗證機制](#token-驗證機制)
5. [錯誤處理與回應格式](#錯誤處理與回應格式)

---

## 專案架構說明
程式碼主要分散於以下位置：
- `api/models.py`：定義資料庫模型 (Order, Product, OrderProduct, OrderNumberSequence)
- `api/views_order.py`：與訂單相關的 API (import_order, order_detail)
- `api/views_product.py`：與產品相關的 API (create_product, delete_product)
- `api/auth_utils.py`：負責 Token 驗證的 decorator 與函式
- `api/utils.py`：通用工具函式 (JSON parsing、訂單編號生成)

---

## 資料庫結構

### 1. Order (訂單表)
| 欄位名稱     | 型別                               | 說明                              |
|-------------|------------------------------------|-----------------------------------|
| id          | PK (Django AutoField)              | Django 內建的 Primary Key         |
| order_number| `CharField(max_length=20, unique=True)` | 訂單編號，格式例如 `ORD2025031700001`       |
| total_price | `DecimalField(max_digits=10, decimal_places=2)` | 訂單總金額                       |
| created_time| `DateTimeField(auto_now_add=True)` | 建立時間，建立時自動寫入          |
| username    | `CharField(max_length=50)`   | 下單人的使用者名稱（必填）           |
| status      | `CharField(max_length=20, default='CREATED')` | 訂單狀態，預設為 "CREATED" |
- **說明**：  
  - `order_number` 的生成邏輯由 `generate_order_number()` 處理，確保每天編號都從 1 開始累加。
  - `total_price` 會在 `import_order` 函式執行後，將訂單中所有產品金額加總後寫入。
  - `username` 表示建立該訂單的用戶，需於下單時傳入，否則 API 會回傳錯誤。
  - `status` 表示訂單狀態，目前預設固定為 `'CREATED'`，未來可擴充其他狀態。

---

### 2. Product (產品表)
| 欄位名稱     | 型別                               | 說明                   |
|-------------|------------------------------------|------------------------|
| id          | PK (Django AutoField)              | Django 內建的 Primary Key |
| product_id  | `CharField(max_length=20, unique=True)` | 產品編號 (自訂)，必須唯一 |
| name        | `CharField(max_length=255)`        | 產品名稱               |
| description | `TextField(blank=True)`            | 產品描述，可為空       |
| price       | `DecimalField(max_digits=10, decimal_places=2)` | 產品單價             |
| stock       | `PositiveIntegerField(default=0)`  | 產品庫存，預設為 0     |
| created_time| `DateTimeField(auto_now_add=True)` | 建立時間               |

- **說明**：  
  - `product_id` 與 `order_number` 類似，具有唯一性。
  - `price` 為單一產品之單價，當下單時會紀錄在 `OrderProduct.price_at_order_time`。
  - `stock` 表示目前產品可供下單的庫存數量，**下訂單時會自動扣減**，若庫存不足將無法下單。

---

### 3. OrderProduct (訂單與產品關係表)
| 欄位名稱          | 型別                                 | 說明                                             |
|------------------|--------------------------------------|--------------------------------------------------|
| id               | PK (Django AutoField)                | Django 內建的 Primary Key                        |
| order            | `ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')`   | 關聯至 **Order** 表                               |
| product          | `ForeignKey(Product, on_delete=models.CASCADE, related_name='product_orders')` | 關聯至 **Product** 表                             |
| quantity         | `PositiveIntegerField()`             | 該產品在此訂單中的數量                           |
| price_at_order_time | `DecimalField(max_digits=10, decimal_places=2)` | 下單當時單價（保留下單時的即時價格） |

- **說明**：  
  - `unique_together = ('order', 'product')` 代表同一張訂單不能重複出現同樣的產品紀錄。
  - 建立訂單時，同時建立多筆 `OrderProduct` 對應多項產品。
  - `price_at_order_time` 記錄下單當時單價，產品後續調價不影響已下訂單之紀錄。

---

### 4. OrderNumberSequence (訂單編號序號表)
| 欄位名稱     | 型別                                  | 說明                                               |
|-------------|---------------------------------------|---------------------------------------------------|
| id          | PK (Django AutoField)                 | Django 內建的 Primary Key                          |
| date        | `CharField(max_length=8, unique=True)`| 儲存日期字串，格式 `YYYYMMDD`                      |
| sequence    | `IntegerField(default=1)`             | 依每日累加的序號，於產生訂單編號時會自動加 1        |

- **說明**：  
  - 當天尚未有任何訂單紀錄時，會自動產生一筆 (date=當天, sequence=1)。
  - 已存在後，每次生成訂單號時都會 `sequence += 1`。

---

## API 說明

### 1. 建立產品 (POST /api/create-product/)
**位置**：`api/views_product.py` → `create_product`

**功能**：建立新產品。

**Request JSON 範例**：
```json
{
    "access_token": "omni_pretest_token",
    "product_id": "PDT001",
    "name": "Sample Product",
    "description": "This is a test product",
    "price": 100.00,
    "stock": 10
}
```

|  欄位名稱    |  說明                           | 必填 |
|-------------|--------------------------------|-----|
| access_token| 用於 API 驗證，固定為 "omni_pretest_token" | 是   |
| product_id  | 產品編號，需唯一               | 是   |
| name        | 產品名稱                        | 是   |
| description | 產品描述，預設可為空            | 否   |
| price       | 單價（Decimal）                 | 是   |
| stock       | 庫存數量（正整數，預設為 0）    | 否   |

**成功回應** (HTTP 201)：
```json
{
    "message": "Product created successfully",
    "product_id": "PDT001"
}
```

**錯誤回應**：
1. 缺少欄位 (HTTP 400)：
   ```json
   {
     "error": "Missing required fields"
   }
   ```
2. Token 驗證失敗 (HTTP 403)：
   ```json
   {
     "error": "Invalid access token"
   }
   ```
3. JSON 格式錯誤 (HTTP 400)：
   ```json
   {
     "error": "Invalid JSON format"
   }
   ```

---

### 2. 刪除產品 (DELETE /api/delete-product/)
**位置**：`api/views_product.py` → `delete_product`

**功能**：刪除指定的產品。

**Request JSON 範例**：
```json
{
    "access_token": "omni_pretest_token",
    "product_id": "PDT001"
}
```

|  欄位名稱    |  說明                           | 必填 |
|-------------|--------------------------------|-----|
| access_token| 用於 API 驗證                  | 是   |
| product_id  | 欲刪除的產品編號               | 是   |

**成功回應** (HTTP 200)：
```json
{
    "message": "Product PDT001 deleted successfully"
}
```

**錯誤回應**：
1. 缺少欄位 (HTTP 400)：
   ```json
   {
     "error": "Missing product_id"
   }
   ```
2. 產品不存在 (HTTP 404)：
   ```json
   {
     "error": "Product PDT001 does not exist."
   }
   ```
3. Token 驗證失敗 (HTTP 403)：
   ```json
   {
     "error": "Invalid access token"
   }
   ```
4. JSON 格式錯誤 (HTTP 400)：
   ```json
   {
     "error": "Invalid JSON format"
   }
   ```

---

### 3. 匯入訂單 (POST /api/import-order/)
**位置**：`api/views_order.py` → `import_order`

**功能**：從前端接收產品清單，產生一張訂單，並計算總金額。

**Request JSON 範例**：
```json
{
    "access_token": "omni_pretest_token",
    "username": "test_user",
    "products": [
        { "product_id": "PDT001", "quantity": 2 },
        { "product_id": "PDT002", "quantity": 1 }
    ]
}
```

|   欄位名稱   |    說明                             | 必填 |
|-------------|--------------------------------------|-----|
| access_token| 用於 API 驗證，固定為 "omni_pretest_token" | 是   |
| username    | 下單的使用者名稱                      | 是  |
| products    | 產品清單 Array                      | 是   |
| product_id  | 產品編號                            | 是   |
| quantity    | 此產品數量                           | 是   |

**成功回應** (HTTP 201)：
```json
{
    "message": "Order created successfully",
    "order_number": "ORD2025031700001",
    "total_price": 300.0
}
```

**錯誤回應**：
1. JSON 格式錯誤 (HTTP 400)：
   ```json
   {
     "error": "Invalid JSON format"
   }
   ```
2. Token 驗證失敗 (HTTP 403)：
   ```json
   {
     "error": "Invalid access token"
   }
   ```
3. 缺少 `products` 或單一產品中缺少 `product_id`/`quantity` (HTTP 400)：
   ```json
   {
     "error": "No products provided"
   }
   ```
   或
   ```json
   {
     "error": "Each product must contain product_id and quantity."
   }
   ```
4. 指定的 `product_id` 不存在 (HTTP 400)：
   ```json
   {
     "error": "Product PDT999 does not exist."
   }
   ```
5. 缺少 'username' (HTTP 400)：
   ```json
   {
     "error": "Username is required"
   }
   ```
6. 產品庫存不足 (HTTP 400)：
   ```json
   {
     "error": "Insufficient stock for product PDT002."
   }
   ```

---

### 4. 查詢訂單 (GET /api/order-detail/<order_number>/)
**位置**：`api/views_order.py` → `order_detail`

**功能**：查詢特定訂單的詳細資訊。

**成功回應** (HTTP 200)：
```json
{
    "order_number": "ORD2025031700001",
    "total_price": 300.0,
    "created_time": "2025-03-17T10:25:30.123456Z",
    "products": [
        {
            "product_name": "Sample Product A",
            "quantity": 2,
            "price_at_order_time": 100.0
        },
        {
            "product_name": "Sample Product B",
            "quantity": 1,
            "price_at_order_time": 100.0
        }
    ]
}
```

| 欄位名稱               | 說明                              |
|------------------------|-----------------------------------|
| order_number           | 查詢的訂單編號                    |
| total_price            | 訂單總金額                        |
| created_time           | 訂單建立時間                      |
| products               | 產品清單                          |
| product_name           | 產品名稱                          |
| quantity               | 該產品在此訂單中的數量            |
| price_at_order_time    | 下單當時的單價                    |

**錯誤回應**：
1. 若該 `order_number` 不存在 (HTTP 404)：
   ```json
   {
     "error": "Order not found"
   }
   ```

---

## Token 驗證機制
- 預設可用的 Token：`"omni_pretest_token"`
- 驗證邏輯由 `@validate_access_token` decorator 實現：
  1. 先解析 JSON (失敗則回傳 400)
  2. 取得 `access_token`
  3. 比對是否符合預設值，若不符回傳 403

---