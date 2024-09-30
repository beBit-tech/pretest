from api.adapter.repository.product.product_model import Product
from api.use_case.repository.repository_interface import RepositoryInterface

class ProductRepository(RepositoryInterface):
    def add(self, data_map: dict):
        existing_product = Product.objects.filter(name=data_map.get('name')).first()

        if existing_product:
            raise ValueError(f"Product with name '{data_map.get('name')}' already exists.")
        
        Product.objects.create(**data_map)

    def get_by_number(self, number: str) -> dict:
        try:
            
            product = Product.objects.get(number=number)
            return {
                'number': product.number,
                'price': product.price,
            }
        except Product.DoesNotExist:
            raise Exception(f"Product with number {number} not found")

    def check_products_exist(self, product_numbers: list) -> set:
        existing_products = Product.objects.filter(number__in=product_numbers)
        existing_numbers = set(existing_products.values_list('number', flat=True))
        missing_numbers = set(product_numbers) - existing_numbers
        
        return missing_numbers