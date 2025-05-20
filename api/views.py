from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import ImportOrderSerializer


ACCEPTED_TOKEN = ('omni_pretest_token')

def auth_validation(token):
    return token == ACCEPTED_TOKEN


@api_view(['POST', 'GET'])  # GET added for web display
def import_order(request):
    if request.method == 'POST':
        import_order_serializer = ImportOrderSerializer(data=request.data)

        if import_order_serializer.is_valid():
            if auth_validation(import_order_serializer.validated_data['token']):
                # print(import_order_serializer.validated_data['order'])
                import_order_serializer.save()

                return Response(import_order_serializer.data['order'], status=status.HTTP_200_OK)
            else:
                return Response('Token Invalid', status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(import_order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else: return Response('GET')