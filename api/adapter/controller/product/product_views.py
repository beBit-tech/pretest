from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.adapter.controller.decoractor import token_required
from api.adapter.controller.product.product_serializer import ProductSerializer
from api.use_case.product.create_product import CreateProduct
from api.use_case.product.create_product_input import CreateProductInput
from api.use_case.product.create_product_output import CreateProductOutput
from api.adapter.repository.product.product_repository import ProductRepository

@token_required
@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data = request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        product_name = validated_data["name"]
        product_price = validated_data["price"]
        
        input = CreateProductInput(name = product_name, price = product_price)
        repo = ProductRepository()
        output: CreateProductOutput = CreateProduct(repo).execute(input = input)
    
        if output.result:
            return Response({
                'product_number': output.product_number,
                'message': 'Product created successfully.'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'error': str(output.exception),
                'message': 'Product creation failed.'
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)