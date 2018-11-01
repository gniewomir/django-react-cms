from rest_framework.viewsets import ModelViewSet

from .models import ComponentInstance, ComponentType, Scene
from .serializers import ComponentInstanceSerializer, ComponentTypeSerializer, SceneSerializer


class TypeView(ModelViewSet):
    serializer_class = ComponentTypeSerializer
    queryset = ComponentType.objects.all()


class ComponentView(ModelViewSet):
    serializer_class = ComponentInstanceSerializer
    queryset = ComponentInstance.objects.all()


class SceneView(ModelViewSet):
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()
