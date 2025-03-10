import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from rest_framework.decorators import api_view
from api.models import Order, Product
from api.decorators import api_token_required
from django.utils.timezone import now
# Create your views here.

@api_view(["POST"])
@api_token_required

def import_order(request):
    data = request.data

    order_number = data.get("order_number")
    total_price = data.get("total_price")
    customer_name = data.get("customer_name")
    customer_email = data.get("customer_email")
    product_ids = data.get("product_ids", [])

    if not order_number or not total_price or not customer_name or not customer_email:
        return HttpResponseBadRequest(
            json.dumps({"Error": "Missing Required Fields"}), 
            content_type = "application/json"
        )

    try:
        total_price = float(total_price)

        order = Order.objects.create(
            order_number = order_number,
            total_price = total_price,
            customer_name = customer_name,
            customer_email = customer_email,
            created_time = now()
        )

        products = Product.objects.filter(id__in = product_ids)
        order.products.set(products)

        return HttpResponse(
            json.dumps({
                "order_number": order.order_number,
                "total_price": order.total_price,
                "customer_name": order.customer_name,
                "customer_email": order.customer_email,
                "products": [p.name for p in order.products.all()],
                "created_time": order.created_time.strftime('%Y-%m-%d %H:%M:%S')
            }),
            status = 201,
            content_type = "application/json"
        )

    except Exception as e:
        return HttpResponseBadRequest(
            json.dumps({"Error": str(e)}), 
            content_type = "application/json"
        )
