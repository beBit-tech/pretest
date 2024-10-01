from typing import List
from api.adapter.repository.order.order_model import Order, OrderProduct
from api.use_case.repository.repository_interface import RepositoryInterface

class OrderRepository(RepositoryInterface):
    def add(self, data_map: dict):
        try:
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
        except Exception as e:
            raise Exception(f"Failed to add order: {str(e)}")
        
    def get_all(self) -> List[dict]:
        try:
            orders = Order.objects.prefetch_related('orderproduct_set').all()
            result = []

            for order in orders:
                order_products = order.orderproduct_set.all()
                order_lines = [
                    {
                        "number": order_product.product_number_id,
                        "quantity": order_product.quantity
                    }
                    for order_product in order_products
                ]
                result.append(
                    {
                        "number": order.number,
                        "total_price": order.total_price,
                        "created_time": order.created_time,
                        "order_lines": order_lines
                    }
                )
                
            return result
        except Exception as e:
            raise Exception(f"Failed to retrieve orders: {str(e)}")