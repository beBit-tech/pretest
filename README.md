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

* Feel free to let us know if there is any question: shelby.xiao@omniscientai.com
---
## API Endpoints

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
        2. `400`: (Complete or Failed -> Failed)

> [!NOTE]
> 所有 UUID 參數需要以有效的 UUID 格式傳遞，否則將回傳404錯誤訊息。
---
## DB Details
1. `db.png`
2. [dbdocs](https://dbdocs.io/robertmadhead0919/Omni_Pretest?schema=public&view=relationships&table=api_product)

## Test Coverage
1. `test_coverage.png`
2. `htmlcov/index.html`


<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Coverage report</title>
    <link rel="icon" sizes="32x32" href="favicon_32_cb_58284776.png">
    <link rel="stylesheet" href="style_cb_8e611ae1.css" type="text/css">
</head>
<body class="indexfile">
<header>
    <div class="content">
        <h1>Coverage report:
            <span class="pc_cov">99%</span>
        </h1>
        <p class="text">
            <a class="nav" href="https://coverage.readthedocs.io/en/7.7.0">coverage.py v7.7.0</a>,
            created at 2025-03-21 11:41 +0000
        </p>
    </div>
</header>
<main id="index">
    <table class="index" data-sortable>
        <thead>
            <tr class="tablehead" title="Click to sort">
                <th id="file" class="name left" aria-sort="none" data-shortcut="f">File<span class="arrows"></span></th>
                <th id="statements" aria-sort="none" data-default-sort-order="descending" data-shortcut="s">statements<span class="arrows"></span></th>
                <th id="missing" aria-sort="none" data-default-sort-order="descending" data-shortcut="m">missing<span class="arrows"></span></th>
                <th id="excluded" aria-sort="none" data-default-sort-order="descending" data-shortcut="x">excluded<span class="arrows"></span></th>
                <th id="coverage" class="right" aria-sort="none" data-shortcut="c">coverage<span class="arrows"></span></th>
            </tr>
        </thead>
        <tbody>
            <tr class="region">
                <td class="name left"><a href="z_10fae538ba4e8521___init___py.html">api/__init__.py</a></td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="0 0">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_10fae538ba4e8521_admin_py.html">api/admin.py</a></td>
                <td>5</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="5 5">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_10fae538ba4e8521_apps_py.html">api/apps.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_e38ba9b706ec887b_0001_initial_py.html">api/migrations/0001_initial.py</a></td>
                <td>8</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="8 8">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_e38ba9b706ec887b_0002_alter_product_title_py.html">api/migrations/0002_alter_product_title.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_e38ba9b706ec887b_0003_order_payment_status_alter_orderitem_order_py.html">api/migrations/0003_order_payment_status_alter_orderitem_order.py</a></td>
                <td>5</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="5 5">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_e38ba9b706ec887b_0004_rename_payment_status_order_status_py.html">api/migrations/0004_rename_payment_status_order_status.py</a></td>
                <td>4</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="4 4">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_e38ba9b706ec887b_0005_alter_order_total_price_and_more_py.html">api/migrations/0005_alter_order_total_price_and_more.py</a></td>
                <td>5</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="5 5">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_e38ba9b706ec887b_0006_alter_product_price_py.html">api/migrations/0006_alter_product_price.py</a></td>
                <td>5</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="5 5">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_e38ba9b706ec887b_0007_alter_order_total_price_and_more_py.html">api/migrations/0007_alter_order_total_price_and_more.py</a></td>
                <td>5</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="5 5">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_e38ba9b706ec887b___init___py.html">api/migrations/__init__.py</a></td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="0 0">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_10fae538ba4e8521_models_py.html">api/models.py</a></td>
                <td>29</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="29 29">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_10fae538ba4e8521_serializers_py.html">api/serializers.py</a></td>
                <td>46</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="46 46">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_10fae538ba4e8521_tests_py.html">api/tests.py</a></td>
                <td>119</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="119 119">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_10fae538ba4e8521_urls_py.html">api/urls.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_10fae538ba4e8521_util_py.html">api/util.py</a></td>
                <td>11</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="11 11">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_10fae538ba4e8521_views_py.html">api/views.py</a></td>
                <td>85</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="85 85">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="manage_py.html">manage.py</a></td>
                <td>11</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="9 11">82%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_d4bc3815bc24b3f3___init___py.html">pretest/__init__.py</a></td>
                <td>0</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="0 0">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_d4bc3815bc24b3f3_settings_py.html">pretest/settings.py</a></td>
                <td>19</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="19 19">100%</td>
            </tr>
            <tr class="region">
                <td class="name left"><a href="z_d4bc3815bc24b3f3_urls_py.html">pretest/urls.py</a></td>
                <td>3</td>
                <td>0</td>
                <td>0</td>
                <td class="right" data-ratio="3 3">100%</td>
            </tr>
        </tbody>
        <tfoot>
            <tr class="total">
                <td class="name left">Total</td>
                <td>371</td>
                <td>2</td>
                <td>0</td>
                <td class="right" data-ratio="369 371">99%</td>
            </tr>
        </tfoot>
    </table>
</main>
</body>
</html>
