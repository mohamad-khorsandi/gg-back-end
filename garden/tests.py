from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from garden.models import Garden
from accounts.models import GardenOwner


class GardenGetIDAPITest(APITestCase):
    def setUp(self):
        self.user1 = GardenOwner.objects.create(name='Test Garden Owner 1', email='test1@test.com', password='1234')
        self.garden_owner1 = self.user1.gardenownerprofile
        self.user2 = GardenOwner.objects.create(name='Test Garden Owner 2', email='test2@test.com', password='1234')
        self.garden_owner2 = self.user2.gardenownerprofile
        self.garden = Garden.objects.create(name='Test Garden 1', is_verified=True, garden_owner=self.garden_owner1)
        self.unverified_garden = Garden.objects.create(name='Test Garden 2', is_verified=False, garden_owner=self.garden_owner2)

    def test_get_garden_by_id(self):
        url = reverse('garden:get_garden_by_id_api', kwargs={'id': self.garden.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Garden 1')

    def test_get_garden_by_id_with_invalid_id(self):
        url = reverse('garden:get_garden_by_id_api', kwargs={'id': 999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_garden_by_id_with_invalid_garden_verification(self):
        url = reverse('garden:get_garden_by_id_api', kwargs={'id': self.unverified_garden.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
