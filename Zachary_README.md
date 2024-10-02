# Omni Pretest

## 介紹
本次 Omni Pretest 共完成以下幾點內容：
- [依照 **Clean Architecture** 架構與規則對專案進行拆分及開發](#clean-architecture)
- [使用 TDD 進行開發，完成單元測試與 API 測試，並新增專門執行單元測試的 test runner 將單元測試跟資料庫解耦合](#tdd)
- [針對 Order、Product 的操作新增 5 隻 API](#api)
- [使用 decorator 檢查 token](#decorator)
- [使用 PGAdmin 檢視資料庫](#pgadmin)

以下將針對上述內容依序進行說明。

---
## Clean Architecture
本專案基於 **Clean Architecture**，將系統劃分為 **Entity 層**、**Use Case 層**、**Adapter 層**。各層負責的功能如下：

- **Entity 層**：負責存放領域核心物件。
- **Use Case 層**：包含對核心物件的操作邏輯。
- **Adapter 層**：處理外部系統交互和具體技術細節。

### Entity 層

位於 `api/entity/`，負責存放領域中的核心物件：

- `Order`：訂單物件
- `Product`：產品物件

### Use Case 層

位於 `api/use_case/`，負責定義對 Entity 層進行操作的具體服務，以及處理與 Adapter 層之間的依賴反轉。

- **業務規則**
  - **訂單僅可提及已存在於資料庫內的產品**

- **服務清單**：
  - `import_order`
  - `get_all_orders`
  - `delete_order`
  - `create_product`
  - `get_all_products`

- **依賴反轉介面**：
  - `RepositoryInterface`：負責與 Adapter 層資料庫解耦，提供依賴反轉的接口。

### Adapter 層
位於 `api/adapter/`，負責處理與外部系統的交互，包括資料庫操作和請求處理。具體內容如下：

- **資料庫操作**：
  - `api/adapter/repository/`：存放 Django 架構下的 `models`，負責資料庫交互。
  
- **請求處理**：
  - `api/adapter/controller/`：儲存 Django 架構下的 `views`，負責 HTTP 請求的處理。


---
## TDD

本專案採用 **TDD**（測試驅動開發）進行開發，但省略了對物件創建的測試。測試分為 **單元測試** 和 **API 測試**，具體如下：

### 單元測試

所有單元測試皆繼承自 `SimpleTestCase`，並且搭配 `Test Double` 確保單元測試聚焦於核心邏輯，不依賴資料庫。

- **單元測試路徑**：`api/tests/unit_test/`
- **Test Double**：`api/tests/test_double` 中存放資料庫替身，模擬資料庫操作，使測試專注於業務邏輯。
  
由於 Django 預設測試會搭配資料庫一起執行，為了讓單元測試完全與資料庫解耦，特別在 `core/runner/` 新增了一個自定義的 **Test Runner**。該 Runner 專門執行繼承自 `SimpleTestCase` 的測試，並且不會啟動資料庫。

- 於`${PATH_TO_PRETEST}`目錄下執行單元測試指令：
  ```bash
  python manage.py unit_test
  ```
### API 測試
API 測試目的在驗證系統與外部的交互，測試案例會使用 Django 的默認測試框架，並搭配資料庫執行。

- **API測試路徑**：`api/tests/api_test/`
- 於`${PATH_TO_PRETEST}`目錄下執行單元測試指令：
  ```bash
  python manage.py test
  ```
---
## API
本次專案共新增了 [`Import Order`](#api-import-order)、[`Get All Orders`](#api-get-all-orders)、[`Delete Order`](#api-delete-order)、[`Create Product`](#api-create-product)、[`Get All Products`](#api-get-all-products)五隻 API，以下依序對這五隻 API 進行說明。

### API: Import Order

#### 說明
此 API 用於創建一個新的訂單。根據訂單總價、創建時間以及訂單明細來創建訂單。

#### URL 
POST /api/import-order/

#### 認證
此 API 需要認證，用戶必須提供有效的 API token 來進行授權。
- **Authorization**: `omni_pretest_token`

#### 請求格式

**Content-Type**: `application/json`

#### 請求 Body

| 參數            | 類型         | 必填 | 說明                   |
| --------------- | ------------ | ---- | ---------------------- |
| `total_price`   | `float`      | 是   | 訂單總價             |
| `created_time`  | `datetime`   | 是   | 訂單創建時間         |
| `order_lines`   | `list`       | 是   | 訂單明細     |

##### `order_lines` 結構

每個 `order_line` 應包含以下內容：

| 參數          | 類型         | 必填 | 說明                   |
| ------------- | ------------ | ---- | ---------------------- |
| `product_id`  | `string`     | 是   | 產品 UUID      |
| `quantity`    | `int`        | 是   | 產品數量       |

### 範例請求

```json
{
    "total_price": 44.5,
    "created_time": "2024-10-01T10:00:00",
    "order_lines": [
        {
            "number": "73206538-c3fa-4b4a-8254-2dc13432e573",
            "quantity": 2
        },
        {
            "number": "88c55799-99aa-48e7-9925-70bc6e44b1a8",
            "quantity": 3
        }
    ]
}
```
### 成功回應
**Code**: 201 CREATED

**Content example:**
```json
{
  "number": "cbbdfb88-814e-4978-b0bc-3829871db56f",
  "message": "Create order successfully."
}
```

### 失敗回應
**Contition**: 欄位缺失

**Code**: 400 BAD REQUEST

**Content example:**
```json
{
  "total_price": [
    "A valid number is required."
  ]
}
```

**Contition**: 產品編號不存在

**Code**: 400 BAD REQUEST

**Content example:**
```json
{
  "error": "Product 123 not exist",
  "message": "Create order failed."
}
```

**Contition**: Token 缺失

**Code**: 401 UNAUTHORIZED

**Content example:**
```json
{
  "error": "Token is missing"
}
```

### API: Get All Orders

#### 說明
此 API 用於取回所有訂單。

#### URL 
GET /api/orders/

#### 認證
此 API 需要認證，用戶必須提供有效的 API token 來進行授權。
- **Authorization**: `omni_pretest_token`

### 成功回應
**Code**: 200 OK

**Content example:**
```json
{
  "orders": [
    {
      "number": "667d3905-5a4c-46de-a95f-7c545f6e343d",
      "total_price": 44.5,
      "created_time": "2024-10-01T10:00:00Z",
      "order_lines": [
        {
          "number": "73206538-c3fa-4b4a-8254-2dc13432e573",
          "quantity": 2
        },
        {
          "number": "88c55799-99aa-48e7-9925-70bc6e44b1a8",
          "quantity": 3
        }
      ]
    },
    {
      "number": "31c5673d-ed6b-45e7-9b66-b7ffa5006e14",
      "total_price": 44.5,
      "created_time": "2024-10-01T10:00:00Z",
      "order_lines": [
        {
          "number": "73206538-c3fa-4b4a-8254-2dc13432e573",
          "quantity": 2
        },
        {
          "number": "88c55799-99aa-48e7-9925-70bc6e44b1a8",
          "quantity": 3
        }
      ]
    }
  ],
  "message": "Fetch orders successfully."
}
```

### 失敗回應
**Contition**: Token 缺失

**Code**: 401 UNAUTHORIZED

**Content example:**
```json
{
  "error": "Token is missing"
}
```

### API: Delete Order

#### 說明
此 API 用於根據訂單編號刪除指定的訂單。

#### URL 
DELETE /api/orders/{number}/

#### URL 參數

| 參數      | 類型   | 必填 | 說明             |
| --------- | ------ | ---- | ---------------- |
| `number`  | string | 是   | 訂單 UUID |

#### 認證
此 API 需要認證，用戶必須提供有效的 API token 來進行授權。
- **Authorization**: `omni_pretest_token`

### 成功回應
**Code**: 200 OK

**Content example:**
```json
{
  "message": "Delete order successfully."
}
```

### 失敗回應
**Contition**: Order 編號不存在

**Code**: 400 BAD REQUEST

**Content example:**
```json
{
  "error": "Order with number cbb88-814e-4978-b0bc-3829871db56f does not exist.",
  "message": "Delete order failed."
}
```

**Contition**: Token 缺失

**Code**: 401 UNAUTHORIZED

**Content example:**
```json
{
  "error": "Token is missing"
}
```

### API: Create Product

#### 說明
此 API 用於創建一個新的產品，根據提供的產品名稱和價格來生成一個產品記錄。

#### URL 
POST /api/products/

#### 認證
此 API 需要認證，用戶必須提供有效的 API token 來進行授權。
- **Authorization**: `omni_pretest_token`

#### 請求 Body

| 參數      | 類型    | 必填 | 說明           |
| --------- | ------- | ---- | -------------- |
| `name`    | string  | 是   | 產品的名稱     |
| `price`   | float   | 是   | 產品的價格     |

### 範例請求
```json
{
  "name": "Papaya",
  "price": 8.5
}
```

### 成功回應
**Code**: 200 OK

**Content example:**
```json
{
  "number": "cc2f388c-b937-403e-90d9-8904ff4bd395",
  "message": "Product created successfully."
}
```

### 失敗回應
**Contition**: 欄位缺失

**Code**: 400 BAD REQUEST

**Content example:**
```json
{
  "name": [
    "This field may not be blank."
  ]
}
```

**Contition**: 新增重複名稱之商品
**Code**: 400 BAD REQUEST

**Content example:**
```json
{
  "error": "Failed to add product: Product with name 'Papaya' already exists.",
  "message": "Product creation failed."
}
```

**Contition**: 價格為負數
**Code**: 400 BAD REQUEST

**Content example:**
```json
{
  "non_field_errors": [
    "Price must be greater than 0"
  ]
}
```

**Contition**: Token 缺失

**Code**: 401 UNAUTHORIZED

**Content example:**
```json
{
  "error": "Token is missing"
}
```
### API: Get All Products

#### 說明
此 API 用於取回所有商品。

#### URL 
GET /api/prosucts/

#### 認證
此 API 需要認證，用戶必須提供有效的 API token 來進行授權。
- **Authorization**: `omni_pretest_token`

### 成功回應
**Code**: 200 OK

**Content example:**
```json
{
  "products": [
    {
      "number": "73206538-c3fa-4b4a-8254-2dc13432e573",
      "name": "Apple",
      "price": 12.5
    },
    {
      "number": "88c55799-99aa-48e7-9925-70bc6e44b1a8",
      "name": "Banana",
      "price": 8.5
    },
    {
      "number": "cc2f388c-b937-403e-90d9-8904ff4bd395",
      "name": "Papaya",
      "price": 8.5
    }
  ],
  "message": "Fetch products successfully."
}
```

### 失敗回應
**Contition**: Token 缺失

**Code**: 401 UNAUTHORIZED

**Content example:**
```json
{
  "error": "Token is missing"
}
```

## Decorator
將檢查 token 的邏輯封裝成一個 decorator，並放置在 `api/adapter/controller/decorator.py`，負責檢查請求的授權標頭是否包含有效的 token。

## PGAdmin
在 `docker-compose.yml` 新增 PGAdmin 服務，用來檢視資料庫的狀態。