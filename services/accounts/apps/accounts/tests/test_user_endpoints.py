from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User


class RouteTest(APITestCase):

    def setUp(self):
        self.type = User.objects.create()

    def test_retrieve_by_uuid_is_not_smoking(self):
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(reverse('user-list-or-create', args=(self.user.id,)),
                                         format='json').status_code)