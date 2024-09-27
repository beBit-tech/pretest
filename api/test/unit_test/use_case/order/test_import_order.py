# from django.test import SimpleTestCase
# from api.use_case.order.import_order import ImportOrder
# from api.use_case.order.import_order_input import ImportOrderInput
# from api.use_case.order.import_order_output import ImportOrderOutput
# from api.test.test_double.mock_order_repository import MockOrderRepository


# class TestImportOrder(SimpleTestCase):
#     def setUp(self) -> None:
#         self.repo = MockOrderRepository()
    
#     def test_import_order(self):
#         importOrder = ImportOrder(repo = self.repo)
#         # importOrder.