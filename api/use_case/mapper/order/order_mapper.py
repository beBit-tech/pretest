from api.use_case.mapper.mapper_interface import BaseMapper
from api.entity.order.order import Order

class OrderMapper(BaseMapper):
    
    @staticmethod
    def to_dict(entity: Order) -> dict:
        return {
            "number": entity.number,
            "total_price": entity.total_price,
            "created_time": entity.created_time,
            "order_lines": entity.order_lines
        }
    
    @staticmethod
    def from_dict(data_map: dict):
        return Order(number = data_map["number"], total_price= data_map["total_price"], created_time = data_map["created_time"], order_lines = data_map["order_lines"])