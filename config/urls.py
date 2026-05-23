from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

def health_check(request):
    return JsonResponse({"status": "ok"})

schema_view = get_schema_view(
    openapi.Info(
        title="LLM API Documentation",
        default_version="v1",
        description="API для LLM приложения",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("materials/", include("materials.urls", namespace="materials")),
    path("users/", include("users.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)