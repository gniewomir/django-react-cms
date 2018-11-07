from rest_framework.serializers import ModelSerializer

from .models import Site, Route


class SiteSerializer(ModelSerializer):
    class Meta:
        model = Site
        fields = ('id', 'domain')


class RouteSerializer(ModelSerializer):
    class Meta:
        model = Route
        fields = ('id', 'route', 'site', 'component')
