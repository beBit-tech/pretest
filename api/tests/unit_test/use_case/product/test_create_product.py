from django.test import SimpleTestCase

from api.use_case.product.create_product.create_product import CreateProduct
from api.use_case.product.create_product.create_product_input import CreateProductInput
from api.use_case.product.create_product.create_product_output import CreateProductOutput
from api.tests.test_double.mock_product_repository import MockProductRepository


class TestCreateProduct(SimpleTestCase):
    def setUp(self) -> None:
        self.repo = MockProductRepository()
        self.create_product = CreateProduct(repo = self.repo)        
        
    def test_create_product(self):
        name = "Apple"
        price = 12.5
        
        input = CreateProductInput(name = name, price = price)
        output: CreateProductOutput = self.create_product.execute(input = input)
        product_data = self.repo.get_by_number(output.number)
        
        self.assertIsNone(output.exception)
        self.assertTrue(output.result)
        self.assertEqual(product_data["name"], name)
        self.assertEqual(product_data["price"], price)