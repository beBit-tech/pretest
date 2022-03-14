from django.urls import path
from api.views import *
from rest_framework import routers
from django.urls import include

router = routers.SimpleRouter()
router.register("product", ProductViewSet, basename="product")

urlpatterns = [path("import-order/", import_order, name="import_order"), path("", include(router.urls))]
