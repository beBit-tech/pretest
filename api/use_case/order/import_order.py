from api.use_case.repository.repository_interface import RepositoryInterface
from api.use_case.order.import_order_input import ImportOrderInput
from api.use_case.order.import_order_output import ImportOrderOutput

class ImportOrder:
    def __init__(self, repo: RepositoryInterface) -> None:
        self.repo = repo
        
    def execute(self, input: ImportOrderInput) -> ImportOrderOutput:
        pass
    
    
    