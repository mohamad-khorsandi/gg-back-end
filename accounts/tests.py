from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from plants.models import Plant
from .models import TemporaryUser, NormalUser


class AccountsTests(APITestCase):

    def setUp(self):
        self.valid_user_data = {
            'name': 'Mary',
            'email': 'Mary@example.com',
            'phone_number': '09132541212',
            'password': '1234'
        }
        self.plant = Plant.objects.create(name="رز", description="گل", maintenance="در آب وایتکس ریخته شود", type=1,
                                          light_intensity=2,
                                          temperature=20, water=3, growth=1, attention_need=1, season=3,
                                          is_seasonal=False, fragrance=False, pet_compatible=True,
                                          allergy_compatible=True, edible=False, special_condition="ندارد",
                                          is_valid=True)

    def test_user_options(self):

        # --------------------- signup test
        url_signup = reverse('accounts:user_register')
        response_signup = self.client.post(url_signup, data=self.valid_user_data)
        self.assertEqual(response_signup.status_code, status.HTTP_200_OK)
        self.assertTrue(TemporaryUser.objects.filter(email=self.valid_user_data['email']).exists())
