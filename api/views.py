from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order, Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .serializers import Orderserializer
# Create your views here.
class IndexView(APIView):
    def get(self, request):
        permission_classes = (IsAuthenticated,)

        # Generate counts of some of the main objects
        num_order = Order.objects.all().count()
        num_product = Product.objects.all().count()

        context = {
            'num_order': num_order,
            'num_product': num_product,
        }

        # Render the HTML template index.html with the data in the context variable
        return render(request, 'index.html', context=context)

# username=omni, pw=omnipretest
ACCEPTED_TOKEN = ('68ea14f2cd969ead6abe16e96974254691faf729')


@api_view(['GET','POST'])
def import_order(request, format=None):
    # Add your code here
    if request.method == 'GET':
        order = Order.objects.all()
        serializer = Orderserializer(order, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Orderserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponseBadRequest('we cannot process the request')