from api.adapter.repository.order.order_model import Order, OrderProduct
from api.use_case.repository.repository_interface import RepositoryInterface

class OrderRepository(RepositoryInterface):
    def add(self, data_map: dict):
        order = Order.objects.create(
            number = data_map["number"],
            total_price = data_map["total_price"],
            created_time = data_map["created_time"],
        )
        
        for line in data_map["order_lines"]:
            product_number = line["number"]
            quantity = line["quantity"]
            
            OrderProduct.objects.create(
                order_number = order,
                product_number_id = product_number,
                quantity = quantity
            )