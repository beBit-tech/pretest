# adapter/repository.py
from api.adapter.repository.product.product_model import Product  # Import 你定義的 Product 模型
from api.use_case.repository.repository_interface import RepositoryInterface

class ProductRepository(RepositoryInterface):
    def add(self, data_map: dict) -> int:
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
