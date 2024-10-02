from api.use_case.repository.repository_interface import RepositoryInterface
from api.use_case.order.delete_order.delete_order_input import DeleteOrderInput
from api.use_case.order.delete_order.delete_order_output import DeleteOrderOutput

class DeleteOrder:
    def __init__(self, repo: RepositoryInterface) -> None:
        self.repo = repo
        
    def execute(self, input: DeleteOrderInput) -> DeleteOrderOutput:
        try:
            self.repo.delete(number = input.number)
            
        except Exception as e:
            output = DeleteOrderOutput(result = False, exception = e)
            return output
        return DeleteOrderOutput(result = True)