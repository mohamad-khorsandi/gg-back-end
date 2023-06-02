from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
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

        # --------------------- verify code test
        otp_code = TemporaryUser.objects.filter(email=self.valid_user_data['email']).first().code
        url_verify_code = reverse('accounts:verify_code')
        code = {
            'code': otp_code
        }
        response_verify_code = self.client.post(url_verify_code, data=code)
        self.assertEqual(response_verify_code.status_code, status.HTTP_200_OK)
        signup_user = NormalUser.objects.get(email='Mary@example.com')

        # --------------------- login test
        url_user_login = reverse('accounts:user_login')
        data_login = {
            'email': 'Mary@example.com',
            'password': '1234'
        }
        self.client.force_authenticate(user=signup_user)
        response_user_login = self.client.post(url_user_login, data=data_login)
        user_token = response_user_login.data['token']
        login_user = Token.objects.get(key=user_token).user
        self.assertEqual(response_user_login.status_code, status.HTTP_200_OK)
        self.assertTrue(NormalUser.objects.filter(email=data_login['email']).exists())

        # --------------------- save plant test
        url_save_plant = reverse('accounts:saved_plant_list', kwargs={'id_plant': self.plant.id})
        response_save_plant = self.client.put(url_save_plant)
        self.assertEqual(response_save_plant.status_code, status.HTTP_200_OK)
        self.assertTrue(login_user.saved_plants.filter(id=self.plant.id).exists())

        # --------------------- remove save plant test
        url_remove_save_plant = reverse('accounts:remove_saved_plant', kwargs={'id_plant': self.plant.id})
        response_delete_save_plant = self.client.delete(url_remove_save_plant)
        self.assertEqual(response_delete_save_plant.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(login_user.saved_plants.filter(id=self.plant.id).exists())