import uuid
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

class TestImportOrder(SimpleTestCase):
    def setUp(self) -> None:
        self.created_time = datetime.now()
        self.product_repo = MockProductRepository()
        self.order_repo = MockOrderRepository()
        self.importOrder = ImportOrder(order_repo = self.order_repo, product_repo = self.product_repo)
        
    def __prepare_one_product(self, name: str, price: float) -> str:
        create_product = CreateProduct(repo = self.product_repo)
        
        input = CreateProductInput(name = name, price = price)
        output: CreateProductOutput = create_product.execute(input = input)
        
        return output.number
    
    def test_import_order_with_one_existent_product(self):
        product_number = self.__prepare_one_product(name = "Apple", price = 12.5)
        quantity = 3
        total_price = 37.5
        order_lines = [
            {"number": product_number,
             "quantity": quantity}
            ]
        
        input = ImportOrderInput(total_price = total_price, created_time = self.created_time, order_lines = order_lines)
        output: ImportOrderOutput = self.importOrder.execute(input = input)
        order_data = self.order_repo.get_by_number(output.order_number)
        
        self.assertIsNone(output.exception)
        self.assertTrue(output.result)
        self.assertEqual(order_data["total_price"], total_price)
        self.assertEqual(order_data["created_time"], self.created_time)
        self.assertEqual(order_data["order_lines"], order_lines)
        
    def test_import_order_with_one_non_existent_product(self):
        _ = self.__prepare_one_product(name = "Apple", price = 12.5)
        random_uuid = uuid.uuid4()
        quantity = 3
        total_price = 37.5
        order_lines = [
            {"number": random_uuid,
             "quantity": quantity}
            ]
        
        input = ImportOrderInput(total_price = total_price, created_time = self.created_time, order_lines = order_lines)
        output: ImportOrderOutput = self.importOrder.execute(input = input)
        order_data = self.order_repo.get_by_number(output.order_number)
        
        self.assertIsNotNone(output.exception)
        self.assertFalse(output.result)
        self.assertIsNone(order_data)
        
    def test_import_order_with_multiple_existent_product(self):
        product_number_1 = self.__prepare_one_product(name = "Apple", price = 12.5)
        quantity_1 = 3
        product_number_2 = self.__prepare_one_product(name = "Banana", price = 6.5)
        quantity_2 = 2
        total_price = 50.5
        order_lines = [
            {"number": product_number_1,
             "quantity": quantity_1},
            {"number": product_number_2,
             "quantity": quantity_2}
            ]
        
        input = ImportOrderInput(total_price = total_price, created_time = self.created_time, order_lines = order_lines)
        output: ImportOrderOutput = self.importOrder.execute(input = input)
        order_data = self.order_repo.get_by_number(output.order_number)
        
        self.assertIsNone(output.exception)
        self.assertTrue(output.result)
        self.assertEqual(order_data["total_price"], total_price)
        self.assertEqual(order_data["created_time"], self.created_time)
        self.assertEqual(order_data["order_lines"], order_lines)
        
    def test_import_order_with_existent_and_non_existent_product(self):
        product_number = self.__prepare_one_product(name = "Banana", price = 6.5)
        quantity_1 = 2
        _ = self.__prepare_one_product(name = "Apple", price = 12.5)
        random_uuid = uuid.uuid4()
        quantity_2 = 3
        total_price = 37.5
        order_lines = [
            {"number": product_number,
             "quantity": quantity_1},
            {"number": random_uuid,
             "quantity": quantity_2}
            ]
        
        input = ImportOrderInput(total_price = total_price, created_time = self.created_time, order_lines = order_lines)
        output: ImportOrderOutput = self.importOrder.execute(input = input)
        order_data = self.order_repo.get_by_number(output.order_number)
        
        self.assertIsNotNone(output.exception)
        self.assertFalse(output.result)
        self.assertIsNone(order_data)