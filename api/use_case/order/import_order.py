from typing import List

from api.use_case.repository.repository_interface import RepositoryInterface
from api.use_case.order.import_order_input import ImportOrderInput
from api.use_case.order.import_order_output import ImportOrderOutput
from api.use_case.mapper.order.order_mapper import OrderMapper
from api.entity.order.order import Order

class MissingProductError(Exception):
    def __init__(self, product):
        super().__init__(f"Product not exist")

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
            output = ImportOrderOutput(order_number = None, result = False, exception = e)
            return output
        return ImportOrderOutput(order_number = order.number, result = True)
    
    def __check_products_exist(self, product_lines: List[dict]):
        product_numbers = [line["product_number"] for line in product_lines]
        if not self.product_repo.check_products_exist(product_numbers):
            raise MissingProductError