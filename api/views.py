from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import ImportOrderSerializer, OrderSerializer, ProductSerializer


ACCEPTED_TOKEN = ('omni_pretest_token')

def auth_validation(token):
    return token == ACCEPTED_TOKEN


@api_view(['POST'])
def import_order(request):
    import_order_serializer = ImportOrderSerializer(data=request.data)

    if import_order_serializer.is_valid():
        if auth_validation(import_order_serializer.validated_data['token']):
            import_order_serializer.save()

            return Response(import_order_serializer.data['order'], status=status.HTTP_200_OK)
        else:
            return Response('Token Invalid', status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(import_order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def auth_validation_advanced(func):
    def wrapper(request):
        token = request.headers.get('Authorization')
        if token == f'Bearer {ACCEPTED_TOKEN}':
            return func(request)
        else:
            return Response('Token Invalid', status=status.HTTP_401_UNAUTHORIZED)
    return wrapper


@api_view(['POST'])
@auth_validation_advanced
def import_order_advanced(request):
    order_serializer = OrderSerializer(data=request.data)

    if order_serializer.is_valid():
        order_serializer.save()
        return Response(order_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@auth_validation_advanced
def create_product(request):
    product_serializer = ProductSerializer(data=request.data)

    if product_serializer.is_valid():
        product_serializer.save()
        # print(product_serializer.data)
        return Response(product_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
