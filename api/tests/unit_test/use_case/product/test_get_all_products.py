from django.test import SimpleTestCase

from api.use_case.product.create_product.create_product import CreateProduct
from api.use_case.product.create_product.create_product_input import CreateProductInput
from api.use_case.product.get_all_products.get_all_products import GetAllProducts
from api.use_case.product.get_all_products.get_all_products_output import GetAllProductsOutput
from api.tests.test_double.mock_product_repository import MockProductRepository

class TestGetAllProducts(SimpleTestCase):
    def setUp(self) -> None:
        self.repo = MockProductRepository()
        
    def __create_product(self, name: str, price: float) -> str:
        return CreateProduct(repo = self.repo).execute(input = CreateProductInput(name = name, price = price)).number
            
        
    def test_get_all_products(self):
        name_1 = "Apple"
        price_1 = 12.5
        product_number_1 = self.__create_product(name = name_1, price = price_1)
        
        name_2 = "Banana"
        price_2 = 6.5
        product_number_2 = self.__create_product(name = name_2, price = price_2)
        output: GetAllProductsOutput = GetAllProducts(self.repo).execute()

        self.assertIsNone(output.exception)
        self.assertTrue(output.result)
        self.assertEqual(output.products[0]["number"], product_number_1)
        self.assertEqual(output.products[0]["name"], name_1)
        self.assertEqual(output.products[0]["price"], price_1)
        self.assertEqual(output.products[1]["number"], product_number_2)
        self.assertEqual(output.products[1]["name"], name_2)
        self.assertEqual(output.products[1]["price"], price_2)
        
    def test_get_all_products_with_no_product(self):
        output: GetAllProductsOutput = GetAllProducts(self.repo).execute()
        
        self.assertIsNone(output.exception)
        self.assertTrue(output.result)
        self.assertEqual([], output.products)