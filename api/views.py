from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from api.request_serializers import *
from api.response_serializers import *
from django.conf import settings
from functools import wraps
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions


def IsAuthenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get("Authorization") != settings.ACCEPTED_TOKEN:
            return Response({"detail": "Unauthorized"}, status=401)
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view


@swagger_auto_schema(
    methods=["post"],
    request_body=ImoprtOrderSerializer,
    responses={200: ImoprtOrderResponseSerializer},
    operation_summary="建立訂單",
)
@api_view(["POST"])
@IsAuthenticated
def import_order(request):
    serializers = ImoprtOrderSerializer(data=request.data)
    if serializers.is_valid():
        order = serializers.save()
        return Response(ImoprtOrderResponseSerializer(order).data)
    else:
        return Response(serializers.errors, status=400)


from rest_framework import exceptions


class IsAuthenticatedPermission(permissions.BasePermission):
    message = "customizing permission to token authentication"

    def has_permission(self, request, view):
        if not request.headers.get("Authorization"):
            raise exceptions.NotAuthenticated()
        elif request.headers.get("Authorization") != settings.ACCEPTED_TOKEN:
            raise exceptions.AuthenticationFailed()
        else:
            return True


class ProductViewSet(ModelViewSet):
    lookup_url_kwarg = "product_id"

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedPermission]
