from api.use_case.repository.repository_interface import RepositoryInterface
from api.use_case.product.get_all_products.get_all_products_output import GetAllProductsOutput

class GetAllProducts:
    def __init__(self, repo: RepositoryInterface) -> None:
        self.repo = repo

    def execute(self) -> GetAllProductsOutput:
        try:
            products = self.repo.get_all()
        except Exception as e:
            output = GetAllProductsOutput(products = None, result = False, exception = e)
            return output
        return GetAllProductsOutput(products = products, result = True)