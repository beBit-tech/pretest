from api.use_case.repository.repository_interface import RepositoryInterface
from api.use_case.product.create_product_input import CreateProductInput
from api.use_case.product.create_product_output import CreateProductOutput

class CreateProduct:
    def __init__(self, repo: RepositoryInterface) -> None:
        self.repo = repo
        
    def execute(self, input: CreateProductInput) -> CreateProductOutput:
        pass
    
    
    