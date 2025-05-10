from rest_framework.views import APIView
from ..permission import TokenValid
from rest_framework.response import Response
from ..models import Order

class ImportOrderView(APIView):

    # 選擇驗證方式
    
    permission_classes = [TokenValid]

    def get(self,request):

        return Response({"message": "Hello, world!"})

    def post(self,request):

        order_num_ = request.data.get('order_num')
        total_price_ = request.data.get('total_price')
        created_ = request.data.get('created')

        get_order = Order(order_num =order_num_,total_price= total_price_,created=created_)
        get_order.save()


        return Response({"message": "Got some data!","data": request.data})
        
    
        