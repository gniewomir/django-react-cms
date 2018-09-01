from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import ComponentInstance, ComponentType, Scene


class ComponentTypeTest(APITestCase):

    def setUp(self):
        self.type = ComponentType.objects.create(react_name='Body', name='Body')
        self.instance = ComponentInstance.objects.create(type=self.type, name='Base site body')
        self.scene = Scene.objects.create(root_component=self.instance, name='Homepage')

    def test_retrieve_is_not_smoking(self):
        self.assertEqual(status.HTTP_200_OK, self.client.get(reverse('component-type-single', args=(self.type.id,)),
                                                             format='json').status_code)

    def test_retrieve_response(self):
        self.assertEqual(str(self.type.id), self.client.get(reverse('component-type-single', args=(self.type.id,)),
                                                            format='json').data['id'])

    def test_update_fails_for_anonymous(self):
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('component-type-single', args=(self.type.id,)), {},
                                          format='json').status_code)

    def test_list_is_not_smoking(self):
        self.assertEqual(status.HTTP_200_OK, self.client.get(reverse('component-type-list'), format='json').status_code)

    def test_list_response(self):
        self.assertEqual(str(self.type.id),
                         self.client.get(reverse('component-type-list'), format='json').data[0]['id'])
