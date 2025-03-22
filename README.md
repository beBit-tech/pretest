# Omni Pretest
## Setup Environment
* Download [docker](https://www.docker.com/get-started) and Install

* [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this **pretest** project to your own repository

* Clone **pretest** project from your own repository
    ```
    git clone https://github.com/[your own account]/pretest.git
    ```

* Checkout **pretest** directory
    ```
    cd pretest
    ```

* Start docker container
    ```
    docker-compose up
    ```

* Enter activated **pretest-web-1** container
    ```
    docker exec -it pretest-web-1 bash
    ```
    Note:

    * This container codebase is connected to **pretest** project local codebase
    * If you need to migrate migration files or test testcases, make sure do it in **pretest-web-1** container
---
## Requirements
* Construct **Order** Model in **api** app

    The below information is necessary in **Order** model:
    * Order-number
    * Total-price
    * Created-time

* Construct **import_order** api ( POST method )
    * Validate access token from request data
    
        ( accepted token is defined in **api/views.py** )
    * Parse data and Save to corresponding fields
* Construct api unittest

---
## Advanced Requirements ( optional )
* Replace the statement of checking api access token with a decorator

* Extend Order model
    * Construct **Product** model
    * Build relationships between **Order** and **Product** model

* Get creative and Extend anything you want  
---
## Submit
* After receiving this pretest, you have to finish it in 7 days
* Create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) and name it with your name ( 王小明 - 面試 )
* Feel free to let us know if there is any question: sophie.lee@bebit-tech.com
---
## API Endpoints

> [!NOTE]
> 所有 UUID 參數需要以有效的 UUID 格式傳遞，否則將回傳404錯誤訊息。

> [!IMPORTANT]
> 所有requests header必須加上`Authorization: <access_token>`的形式。

### Products API

- **POST** `/api/create-product/`: 創建新的產品。

    - Request Body: 驗證輸入產品名稱、價格及存貨。

    - Response: 返回創建成功的產品名稱、價格及存貨。

- **DELETE** `/api/delete-product/<uuid:product_number>/`: 刪除指定的產品。

    - Path Parameter: product_number - 產品的唯一識別碼。

    - Response: 返回刪除成功或錯誤訊息。

- **PATCH** `/api/update-product/<uuid:product_number>/`: 更新指定產品的資訊。

    - Path Parameter: product_number - 產品的唯一識別碼。

    - Request Body: 需要更新的產品資訊。

    - Response: 返回更新後的產品資訊。
---
### Orders API

- **POST** `/api/import-order/`: 匯入訂單資料。

    - Request Body: 批量訂單資料。

    - Response: 返回匯入結果。

- **GET** `/api/list-orders/`: 獲取所有訂單的列表。

    - Response: 返回包含所有訂單的 JSON 陣列。

- **GET** `/api/get-order-by-number/<uuid:order_number>/`: 根據訂單號查詢訂單。

    - Path Parameter: order_number - 訂單的唯一識別碼。

    - Response: 返回對應的訂單資訊。

- **GET** `/api/get-order-by-product/<uuid:product_number>/`: 根據產品號碼查詢包含該產品的訂單。

    - Path Parameter: product_number - 產品的唯一識別碼。

    - Response: 返回該產品的訂單資訊。

- **DELETE** `/api/delete-order/<uuid:order_number>/`: 將訂單狀態設為交易失敗(容許一天鑑賞期)。

    - Path Parameter: order_number - 訂單的唯一識別碼。

    - Response: 返回更新後訂單狀態
        1. `200`: (Pending -> Failed)。
        2. `400`: (Complete or Failed or 訂單建立時間超過一天 -> Failed)
---
## DB Details
- [dbdocs](https://dbdocs.io/robertmadhead0919/Omni_Pretest?schema=public&view=relationships&table=api_product)

## Test Coverage
```bash
# run in container
coverage run manage.py test && coverage report
```
- more details in **test_coverage.png**
