from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('indicators.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Young Specialists API",
        default_version='v1',
        description="API documentation for Young Specialists project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]