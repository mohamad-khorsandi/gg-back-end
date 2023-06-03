from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Plant


class PlantDetailsTestCase(APITestCase):
    def setUp(self):
        self.plant = Plant.objects.create(name="Rose", description="frower", maintenance="whitex in water", type=1,
                                          light_intensity=2,
                                          temperature=20, water=3, growth=1, attention_need=1, season=3,
                                          is_seasonal=False, fragrance=False, pet_compatible=True,
                                          allergy_compatible=True, edible=False, special_condition="doesnt have",
                                          is_valid=True)
        self.url = reverse('plants:plant_details', kwargs={'id': self.plant.id})

    def test_get_valid_plant_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Plant.objects.get(name='Rose'))
        self.assertEqual(response.data, {'id': 1, 'images': [], 'gardens': [], 'name': 'Rose', 'description': 'frower',
                                         'maintenance': 'whitex in water', 'type': 1, 'light_intensity': 2,
                                         'temperature': 20,
                                         'location_type': 1, 'water': 3, 'growth': 1, 'attention_need': 1, 'season': 3,
                                         'is_valid': True,
                                         'is_seasonal': False, 'fragrance': False, 'pet_compatible': True,
                                         'allergy_compatible': True, 'edible': False,
                                         'special_condition': 'doesnt have',
                                         'wikipedia_link': None, 'main_img': None})
