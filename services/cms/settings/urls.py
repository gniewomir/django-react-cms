from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('', include('apps.routes.urls')),
    path('', include('apps.components.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title='CMS API')),
    path('schema/', get_schema_view(title='CMS API'))
]
