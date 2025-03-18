from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Product, Order, OrderProduct

class CreateProductAPITest(APITestCase):
    """
    測試 create-product API 的所有可能情況
    """

    def setUp(self):
        """
        初始化。
        """
        self.url = reverse("create-product")
        self.valid_token = "omni_pretest_token"

    def test_create_product_success(self):
        """
        測試：傳入正確的 product_id, name, price, access_token 時，預期成功建立商品。
        應回傳 201 並且資料庫也成功新增一筆 Product。
        """
        data = {
            "access_token": self.valid_token,
            "product_id": "PDT001",
            "name": "Sample Product",
            "price": 100.0,
            "description": "Test Description",
            "stock": 10
        }
        response = self.client.post(self.url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertIn("product_id", response.data)
        
        # 驗證資料庫是否真的新增
        self.assertTrue(Product.objects.filter(product_id="PDT001").exists())

    def test_create_product_missing_fields(self):
        """
        測試：缺少必要欄位時（例如缺 product_id），預期回傳 400。
        """
        data = {
            "access_token": self.valid_token,
            "name": "Sample Product",
            "price": 100.0
            # product_id 缺失
        }
        response = self.client.post(self.url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        
        # 這時資料庫不應該新增任何記錄
        self.assertEqual(Product.objects.count(), 0)

    def test_create_product_invalid_token(self):
        """
        測試：傳入錯誤的 Token（不是 omni_pretest_token）。
        預期回傳 403，並且不會新增資料。
        """
        data = {
            "access_token": "wrong_token",
            "product_id": "PDT002",
            "name": "Sample Product 2",
            "price": 200.0
        }
        response = self.client.post(self.url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("error", response.data)
        self.assertEqual(Product.objects.count(), 0)


class ImportOrderAPITest(APITestCase):
    """
    測試 import-order API 的所有可能情況
    """
    def setUp(self):
        self.url = reverse("import-order")
        self.valid_token = "omni_pretest_token"

        # 先建立一些商品，方便測試下單成功
        Product.objects.create(product_id="PDT001", name="Product A", price=100.0, stock=5)
        Product.objects.create(product_id="PDT002", name="Product B", price=200.0, stock=1)

    def test_import_order_success(self):
        """
        測試：正確傳入兩個商品，各自指定數量，預期能成功建立訂單。
        應回傳 201 並在資料庫建立 Order & OrderProduct。
        """
        data = {
            "access_token": self.valid_token,
            "products": [
                {"product_id": "PDT001", "quantity": 2},  # 100 x 2
                {"product_id": "PDT002", "quantity": 1},  # 200 x 1
            ]
        }
        response = self.client.post(self.url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertIn("order_number", response.data)
        self.assertIn("total_price", response.data)
        
        # 檢查資料庫是否新增
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderProduct.objects.count(), 2)

        # 驗證計算出來的 total_price
        created_order = Order.objects.first()
        self.assertEqual(float(created_order.total_price), 400.0)  # 100*2 + 200*1 = 400

        # 驗證庫存是否扣減 (原本 5 -> 下訂 2 -> 剩 3)
        product = Product.objects.get(product_id="PDT001")
        self.assertEqual(product.stock, 3)
        product = Product.objects.get(product_id="PDT002")
        self.assertEqual(product.stock, 0)

    def test_import_order_insufficient_stock(self):
        """
        測試庫存不足的情境。
        PDT001 庫存 5，現在嘗試訂購 6，應該回傳 400 並 rollback 訂單。
        """
        data = {
            "access_token": self.valid_token,
            "products": [
                {"product_id": "PDT001", "quantity": 6},  # 庫存只有 5
            ]
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        # 訂單不應該新增
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderProduct.objects.count(), 0)

    def test_import_order_no_products(self):
        """
        測試：products 為空清單時，預期回傳 400。
        """
        data = {
            "access_token": self.valid_token,
            "products": []
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        # 不應該新增任何訂單
        self.assertEqual(Order.objects.count(), 0)

    def test_import_order_missing_product_id_or_quantity(self):
        """
        測試：products 內部某一筆資料缺少 product_id 或 quantity，應回傳 400 並 rollback 已建的 Order。
        """
        data = {
            "access_token": self.valid_token,
            "products": [
                {"product_id": "", "quantity": 2},  # product_id 為空字串
            ]
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        
        # 不會有任何 Order 與 OrderProduct
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderProduct.objects.count(), 0)

    def test_import_order_product_not_exist(self):
        """
        測試：products 裡有一個不存在的商品 product_id (例如 PDT9999)，應回傳 400 並 rollback。
        """
        data = {
            "access_token": self.valid_token,
            "products": [
                {"product_id": "PDT9999", "quantity": 1}
            ]
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderProduct.objects.count(), 0)

    def test_import_order_invalid_token(self):
        """
        測試：傳入錯誤 Token，預期回傳 403 並且不新增任何訂單。
        """
        data = {
            "access_token": "wrong_token",
            "products": [
                {"product_id": "PDT001", "quantity": 1}
            ]
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("error", response.data)

        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderProduct.objects.count(), 0)

class DeleteProductAPITest(APITestCase):
    """
    測試 delete-product 的 API
    """
    def setUp(self):
        self.url = reverse("delete-product")
        self.valid_token = "omni_pretest_token"

        self.product = Product.objects.create(
            product_id="PDT999",
            name="Test Product",
            price=10.0,
            stock=5
        )

    def test_delete_product_success(self):
        """
        傳入正確 Token 與 product_id，預期成功刪除商品。
        """
        data = {
            "access_token": self.valid_token,
            "product_id": self.product.product_id
        }
        response = self.client.delete(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

        # 確認資料庫刪除
        self.assertFalse(Product.objects.filter(product_id="PDT999").exists())

    def test_delete_product_not_exist(self):
        """
        傳入一個不存在的 product_id，預期回傳 404。
        """
        data = {
            "access_token": self.valid_token,
            "product_id": "PDT_NOPE"
        }
        response = self.client.delete(self.url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_delete_product_invalid_token(self):
        """
        傳入錯誤 Token，預期回傳 403，並不執行任何刪除。
        """
        data = {
            "access_token": "wrong_token",
            "product_id": self.product.product_id
        }
        response = self.client.delete(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(product_id="PDT999").exists())

class OrderDetailAPITest(APITestCase):
    """
    測試 order-detail API
    """
    def setUp(self):
        # 先建立兩個商品
        self.productA = Product.objects.create(product_id="PDT001", name="Product A", price=100.0, stock=5)
        self.productB = Product.objects.create(product_id="PDT002", name="Product B", price=200.0, stock=1)

        # 建立訂單
        self.order = Order.objects.create(order_number="ORD_ABCD1234", total_price=300.0)

        # 在訂單裡加入兩個商品
        OrderProduct.objects.create(
            order=self.order,
            product=self.productA,
            quantity=2,
            price_at_order_time=100
        )
        OrderProduct.objects.create(
            order=self.order,
            product=self.productB,
            quantity=1,
            price_at_order_time=200
        )

        self.detail_url = reverse("order-detail", kwargs={"order_number": "ORD_ABCD1234"})

    def test_order_detail_success(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("order_number", response.data)
        self.assertIn("total_price", response.data)
        self.assertIn("products", response.data)
        products = response.data["products"]
        self.assertEqual(len(products), 2)

    def test_order_detail_not_found(self):
        not_found_url = reverse("order-detail", kwargs={"order_number": "ORD_NOT_EXIST"})
        response = self.client.get(not_found_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)


class MiscInvalidJSONTest(APITestCase):
    """
    測試：若傳入非 JSON 格式的 Body，Decorator 或 parse_json_request 會回傳 400。
    """
    def setUp(self):
        self.valid_token = "omni_pretest_token"
        self.create_product_url = reverse("create-product")

    def test_invalid_json_format(self):
        """
        測試：Body 不是正確 JSON，應回傳 400: {"error": "Invalid JSON format"}
        """
        invalid_json = "{ 'access_token': 'omni_pretest_token', "  # 壞掉的 JSON
        
        response = self.client.post(
            self.create_product_url,
            data=invalid_json, 
            content_type="application/json"
        )

        # 期待 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)