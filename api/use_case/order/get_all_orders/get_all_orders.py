from api.use_case.repository.repository_interface import RepositoryInterface
from api.use_case.order.get_all_orders.get_all_orders_output import GetAllOrdersOutput
class GetAllOrders:
    def __init__(self, repo: RepositoryInterface) -> None:
      self.repo = repo
      
    def execute(self) -> GetAllOrdersOutput:
        try:
            orders = self.repo.get_all()
        except Exception as e:
            output = GetAllOrdersOutput(orders = None, result = False, exception = e)
            return output
        return GetAllOrdersOutput(orders = orders, result = True)