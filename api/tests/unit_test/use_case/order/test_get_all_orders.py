from typing import List
from datetime import datetime
from django.test import SimpleTestCase

from api.use_case.order.import_order.import_order import ImportOrder
from api.use_case.order.import_order.import_order_input import ImportOrderInput
from api.use_case.order.import_order.import_order_output import ImportOrderOutput
from api.tests.test_double.mock_order_repository import MockOrderRepository
from api.tests.test_double.mock_product_repository import MockProductRepository
from api.use_case.product.create_product.create_product import CreateProduct
from api.use_case.product.create_product.create_product_input import CreateProductInput
from api.use_case.product.create_product.create_product_output import CreateProductOutput
from api.use_case.order.get_all_orders.get_all_orders import GetAllOrders
from api.use_case.order.get_all_orders.get_all_orders_output import GetAllOrdersOutput

class TestGetAllOrders(SimpleTestCase):
    def setUp(self) -> None:
        self.created_time = datetime.now()
        self.product_repo = MockProductRepository()
        self.order_repo = MockOrderRepository()
        self.importOrder = ImportOrder(order_repo = self.order_repo, product_repo = self.product_repo)
        
    def __create_product(self, name: str, price: float) -> str:
        output: CreateProductOutput = CreateProduct(repo = self.product_repo).execute(CreateProductInput(name = name, price = price))
        return output.number
    
    def __import_order(self, total_price: float, order_lines: List[dict]):
        output: ImportOrderOutput = ImportOrder(order_repo = self.order_repo, product_repo = self.product_repo).execute(input = ImportOrderInput(total_price = total_price, created_time = self.created_time, order_lines = order_lines))
        
        return output.number
    
    def test_get_all_orders(self):
        product_number_1 = self.__create_product(name = "Apple", price = 12.5)
        quantity_1 = 3
        total_price_1 = 37.5
        order_lines_1 = [
            {
                "number": product_number_1,
                "quantity": quantity_1
            }
        ]
        order_number_1 = self.__import_order(total_price = total_price_1, order_lines = order_lines_1)
        
        product_number_2 = self.__create_product(name = "Banana", price = 6.5)
        quantity_2 = 3
        total_price_2 = 19.5
        order_lines_2 = [
            {
                "number": product_number_2,
                "quantity": quantity_2
            }
        ]
        order_number_2 = self.__import_order(total_price = total_price_2, order_lines = order_lines_2)
        
        output: GetAllOrdersOutput = GetAllOrders(repo = self.order_repo).execute()

        self.assertIsNone(output.exception)
        self.assertTrue(output.result)
        self.assertEqual(output.orders[0]["number"], order_number_1)
        self.assertEqual(output.orders[0]["total_price"], total_price_1)
        self.assertEqual(output.orders[0]["created_time"], self.created_time)
        self.assertEqual(output.orders[0]["order_lines"], order_lines_1)
        self.assertEqual(output.orders[1]["number"], order_number_2)
        self.assertEqual(output.orders[1]["total_price"], total_price_2)
        self.assertEqual(output.orders[1]["created_time"], self.created_time)
        self.assertEqual(output.orders[1]["order_lines"], order_lines_2)
        
    def test_get_all_orders_with_no_order(self):
        output: GetAllOrdersOutput = GetAllOrders(self.order_repo).execute()
        
        self.assertIsNone(output.exception)
        self.assertTrue(output.result)
        self.assertEqual([], output.orders)
    
    