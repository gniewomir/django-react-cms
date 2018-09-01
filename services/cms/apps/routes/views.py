import re

from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Site, Route
from .serializers import SiteSerializer, RouteSerializer


class SiteView(ModelViewSet):
    serializer_class = SiteSerializer
    queryset = Site.objects.all()


class RouteView(ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()

    def get_object(self):
        return super().get_object()

    def retrieve(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return Response(self.get_serializer(self.get_object()).data)
        try:
            site = Site.objects.get(domain=kwargs['domain'])
        except Site.DoesNotExist:
            raise NotFound(detail='Unknown site domain.')
        routes = Route.objects.filter(site=site)
        if not routes.count():
            raise NotFound(detail='Site do not have any routes.')
        for single_route in routes:
            if re.match(r'^{}/?$'.format(single_route.route.replace('<slug>', r'([\w-]+)').strip().rstrip('/')),
                        kwargs['path']):
                return Response(self.get_serializer(single_route).data)
        raise NotFound(detail='No matching route.')
