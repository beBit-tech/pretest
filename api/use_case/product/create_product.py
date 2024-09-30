from api.use_case.repository.repository_interface import RepositoryInterface
from api.use_case.product.create_product_input import CreateProductInput
from api.use_case.product.create_product_output import CreateProductOutput
from api.use_case.mapper.product.product_mapper import ProductMapper
from api.entity.product.product import Product

class CreateProduct:
    def __init__(self, repo: RepositoryInterface) -> None:
        self.repo = repo
        
    def execute(self, input: CreateProductInput) -> CreateProductOutput:
        try:
            product = Product(name = input.name, price = input.price)
            self.repo.add(ProductMapper.to_dict(entity = product))
        except Exception as e:
            output = CreateProductOutput(product_number = None, result = False, exception = e)
            return output
        return CreateProductOutput(product_number = product.number, result = True)