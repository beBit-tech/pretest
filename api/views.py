from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import OrderSerializer
from .tokens import validate_token

# Create your views here.


ACCEPTED_TOKEN = "omni_pretest_token"


@api_view(["POST"])
@validate_token
def import_order(request: Request) -> Response:
    data = request.data

    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"order": serializer.data}, status=status.HTTP_201_CREATED)

    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
