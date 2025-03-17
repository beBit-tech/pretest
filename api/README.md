# API User Cases

### 1. 顧客訂單操作

#### 1.1 作為一名顧客，我希望能夠提交訂單，以購買我需要的商品
- **成功提交訂單，且所有商品庫存充足**
  - 訂單狀態變為 **Processing**（處理中）
  - 返回: `Order imported successfully`
  
- **有商品缺貨**
  - 訂單狀態變為 **Pending**（等待補貨）
  
- **提交相同的訂單編號（order_number）**
  - 返回: `Order XXX already exists`
  
- **訂單中有不存在的商品**
  - 返回: `Products do not exist`

### 2. 管理員商品操作

#### 2.1 作為一名管理員，我希望能夠新增或更新商品，以確保商品資料是最新的
- **商品不存在，創建新商品**
  - 返回: `Product created successfully`
  
- **商品已存在，更新商品資訊**
  - 更新商品後影響訂單狀態：
    - 如果某些訂單原本庫存不足而處於 **Pending**，但更新後庫存充足，則變更為 **Processing**
    - 如果某些訂單原本庫存充足而處於 **Processing**，但更新後庫存不足，則變更為 **Pending**
  - 返回: `Product updated successfully`

#### 2.2 作為一名管理員，我希望能夠刪除商品，以便移除已停售的產品
- **成功刪除商品**
  - 所有包含該商品的訂單應自動標記為 **Cancelled**
  - 返回: `Product deleted successfully`
  
- **商品不存在**
  - 返回: `Product XXX not found`

### 3. 管理員訂單查詢

#### 3.1 作為一名管理員，我希望能夠查詢特定訂單的詳細資訊，以便追蹤訂單狀態
- **訂單存在**
  - 返回: 回傳包含訂單詳細資訊的 JSON 物件
  
- **訂單不存在**
  - 返回: `Order XXX does not exist`
