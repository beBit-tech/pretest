import uuid
from datetime import datetime
from django.test import SimpleTestCase

from api.tests.test_double.mock_order_repository import MockOrderRepository
from api.use_case.order.delete_order.delete_order import DeleteOrder
from api.use_case.order.delete_order.delete_order_input import DeleteOrderInput
from api.use_case.order.delete_order.delete_order_output import DeleteOrderOutput



class TestDeleteOrder(SimpleTestCase):
    def setUp(self) -> None:
        self.created_time = datetime.now()
        self.repo = MockOrderRepository()
        self.order_number = str(uuid.uuid4)
        order_data = {
            "number": self.order_number,
            "total_price": 44.5,
            "created_time": "2024-10-01T10:00:00",
            "order_lines": [
                {
                    "product_number": "73206538-c3fa-4b4a-8254-2dc13432e573",
                    "quantity": 2
                },
                {
                    "product_number": "88c55799-99aa-48e7-9925-70bc6e44b1a8",
                    "quantity": 3
                }
            ]
        }
        self.repo.add(data_map = order_data)
    
    def test_delete_exist_order(self):
        input = DeleteOrderInput(number = self.order_number)
        output: DeleteOrderOutput = DeleteOrder(self.repo).execute(input = input)
        
        self.assertIsNone(output.exception)
        self.assertTrue(output.result)
        self.assertEqual(self.repo.get_all(), [])


    def test_delete_non_existent_order(self):
        self.assertEqual(len(self.repo.get_all()), 1)
        
        invalid_order_number = str(uuid.uuid4())
        input = DeleteOrderInput(number = invalid_order_number)
        output: DeleteOrderOutput = DeleteOrder(self.repo).execute(input = input)
        
        self.assertIsNotNone(output.exception)
        self.assertFalse(output.result)
        self.assertEqual(len(self.repo.get_all()), 1)
