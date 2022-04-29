from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Contact List API",
        default_version="v1",
        description="An API for storing contacts",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@contacts.remote"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/auth/",
        include("accounts.urls", namespace="accounts"),
    ),
    path(
        "api/",
        include("contacts.urls", namespace="contacts"),
    ),
    # PATTERNS FOR DRF_YASG
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # PATTERNS for DRF SPECTACULAR
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
