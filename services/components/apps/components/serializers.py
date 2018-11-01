from rest_framework.serializers import ModelSerializer

from .models import ComponentInstance, ComponentType, Scene


class ComponentInstanceSerializer(ModelSerializer):
    class Meta:
        model = ComponentInstance
        fields = ('id', 'children', 'type', 'name')


class ComponentTypeSerializer(ModelSerializer):
    class Meta:
        model = ComponentType
        fields = ('id', 'react_name', 'allowed_children_types', 'name')


class SceneSerializer(ModelSerializer):
    class Meta:
        model = Scene
        fields = ('id', 'root_component', 'name')
