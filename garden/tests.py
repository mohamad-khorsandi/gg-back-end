from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from garden.models import Garden
from accounts.models import GardenOwner


class GardenGetIDAPITest(APITestCase):
    def setUp(self):
        self.user = GardenOwner.objects.create(name='Test Garden Owner', email='test@test.com', password='1234')
        self.garden_owner = self.user.gardenownerprofile
        self.garden = Garden.objects.create(name='Test Garden', is_verified=True, garden_owner=self.garden_owner)

    def test_get_garden_by_id(self):
        url = reverse('garden:get_garden_by_id_api', kwargs={'id': self.garden.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Garden')

    def test_get_garden_by_id_with_invalid_id(self):
        url = reverse('garden:get_garden_by_id_api', kwargs={'id': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
