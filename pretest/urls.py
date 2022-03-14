"""pretest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    info=openapi.Info(
        title="beBit-tech pretest API",
        default_version="develope",
        description="""
Clients should authenticate by passing the token key in the "Authorization"
HTTP header, prepended with the string "Token ".  For example:\n
`Authorization: omni_pretest_token`\n
The `swagger-ui` view can be found [here](/api/swagger-docs).\n
The `ReDoc` view can be found [here](/api/redoc).\n
""",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path(
        "api/swagger-docs",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
