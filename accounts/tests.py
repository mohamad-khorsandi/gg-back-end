from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from plants.models import Plant
from .models import TemporaryUser, NormalUser
from .serializers import UserLoginSerializer


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

        # --------------------- change password test
        data_change_password = {
            'old_password': '1234',
            'new_password': '4321'
        }
        url_change_password = reverse('accounts:change_password')
        response_change_password = self.client.post(url_change_password, data=data_change_password)
        self.assertEqual(response_change_password.status_code, status.HTTP_200_OK)
        # self.assertEquals(login_user.password, '4321')


# ----------------------------- change password
class ChangePasswordTestCase(APITestCase):
    def setUp(self):
        self.user = NormalUser.objects.create_user(
            name='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_change_password_success(self):
        url = reverse('accounts:change_password')
        data = {
            'old_password': 'testpass',
            'new_password': 'newpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'detail': 'Password changed successfully.'})
        self.user.refresh_from_db()
        self.assertTrue(self.user.password, 'newpass')

    def test_change_password_wrong_old_password(self):
        url = reverse('accounts:change_password')
        data = {
            'old_password': 'testpass2',
            'new_password': 'newpass'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'old_password': ['Wrong password.']})
        self.user.refresh_from_db()
        self.assertTrue(self.user.password, 'newpass')


# ----------------------------- login test
class UserLoginTestCase(APITestCase):
    url = reverse('accounts:user_login')

    def setUp(self):
        self.user = NormalUser.objects.create(
            email='testuser@example.com',
            password='testpassword123'
        )
        self.client = APIClient()

    def test_user_login_success(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_failure(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_serializer_invalid(self):
        data = {
            'email': 'testuser@example.com',
            'password': ''
        }
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_user_login_token_created(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.url, data)
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)


# ----------------------------- signup test
class UserRegistrationViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:user_register')
        self.client = APIClient()
        self.data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'password': 'testpassword123',
            'phone_number': '09132561223',
            'is_garden_owner': False
        }

    def test_user_registration_success(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TemporaryUser.objects.count(), 1)

    def test_user_registration_serializer_invalid(self):
        data = {
            'name': 'Jane Doe',
            'email': 'janedoe@example.com',
            'phone_number': '09132561223',
            'password': '',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TemporaryUser.objects.count(), 0)

    def test_user_registration_code_update(self):
        self.client.post(self.url, self.data)
        temp_user = TemporaryUser.objects.get(email=self.data['email'])
        old_code = temp_user.code
        self.client.post(self.url, self.data)
        temp_user.refresh_from_db()
        new_code = temp_user.code
        self.assertNotEqual(old_code, new_code)

    def test_user_registration_code_creation(self):
        response = self.client.post(self.url, self.data)
        temp_user = TemporaryUser.objects.get(email=self.data['email'])
        self.assertEqual(temp_user.name, self.data['name'])
        self.assertEqual(temp_user.email, self.data['email'])
        self.assertIsNotNone(temp_user.code)


# ----------------------------- save plant test
class SavedPlantListTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:saved_plant_list', kwargs={'id_plant': 1})
        self.client = APIClient()
        self.user = NormalUser.objects.create(name='testuser', password='testpassword', phone_number='testphone')
        self.client.force_authenticate(user=self.user)
        self.plant = Plant.objects.create(name="رز", description="گل", maintenance="در آب وایتکس ریخته شود", type=1,
                                          light_intensity=2,
                                          temperature=20, water=3, growth=1, attention_need=1, season=3,
                                          is_seasonal=False, fragrance=False, pet_compatible=True,
                                          allergy_compatible=True, edible=False, special_condition="ندارد",
                                          is_valid=True)

    def test_add_saved_plant(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.plant, self.user.saved_plants.all())

    def test_add_existing_saved_plant(self):
        self.user.saved_plants.add(self.plant)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.put(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ----------------------------- remove save plant test
class RemoveSavedPlantViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:remove_saved_plant', kwargs={'id_plant': 1})
        self.client = APIClient()
        self.user = NormalUser.objects.create(name='testuser', password='testpassword', phone_number='testphone')
        self.client.force_authenticate(user=self.user)
        self.plant = Plant.objects.create(name="رز", description="گل", maintenance="در آب وایتکس ریخته شود", type=1,
                                          light_intensity=2,
                                          temperature=20, water=3, growth=1, attention_need=1, season=3,
                                          is_seasonal=False, fragrance=False, pet_compatible=True,
                                          allergy_compatible=True, edible=False, special_condition="ندارد",
                                          is_valid=True)

    def test_remove_saved_plant(self):
        self.user.saved_plants.add(self.plant)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(self.plant, self.user.saved_plants.all())

    def test_remove_unsaved_plant(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(self.plant, self.user.saved_plants.all())

    def test_unauthenticated_user(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
