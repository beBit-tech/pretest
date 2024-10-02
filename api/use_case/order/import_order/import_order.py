from typing import List

from api.use_case.repository.repository_interface import RepositoryInterface
from api.use_case.order.import_order.import_order_input import ImportOrderInput
from api.use_case.order.import_order.import_order_output import ImportOrderOutput
from api.use_case.mapper.order.order_mapper import OrderMapper
from api.entity.order.order import Order

class MissingProductError(Exception):
    def __init__(self, product_numbers: set):
        product_numbers = ', '.join(product_numbers)
        super().__init__(f"Product {product_numbers} not exist")

class ImportOrder:
    def __init__(self, order_repo: RepositoryInterface, product_repo: RepositoryInterface) -> None:
        self.order_repo = order_repo
        self.product_repo = product_repo
        
    def execute(self, input: ImportOrderInput) -> ImportOrderOutput:
        try:
            self.__check_products_exist(product_lines = input.order_lines)
            order = Order(created_time = input.created_time, total_price = input.total_price, order_lines = input.order_lines)
            self.order_repo.add(OrderMapper.to_dict(entity = order))
        except Exception as e:
            output = ImportOrderOutput(number = None, result = False, exception = e)
            return output
        return ImportOrderOutput(number = order.number, result = True)
    
    def __check_products_exist(self, product_lines: List[dict]):
        product_numbers = [line["number"] for line in product_lines]
        missing_product_numbers = self.product_repo.check_products_exist(product_numbers)
        if missing_product_numbers:
            raise MissingProductError(missing_product_numbers)