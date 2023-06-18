import json
import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse
from accounts.custom_backend import CustomBackend
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.test import APIClient

from .token_logic import get_user_from_token

from django.contrib.auth import get_user_model

User = get_user_model()



class RegistrationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='existing@example.com',
            password='password',
            gender='M',
            date_of_birth='1990-01-01',
            weight=70,
            height=180.5,
        )

    def test_registration_success(self):
        url = reverse('registration')
        data = {
            'email': 'test@example.com',
            'password': 'password',
            'gender': 'M',
            'date_of_birth': '1990-01-01',
            'weight': 70,
            'height': 180.5,
        }
        response = self.client.post(url, data)

        self.assertEqual(User.objects.get(email='test@example.com').email, 'test@example.com')
        self.assertTrue(User.objects.get(email='test@example.com').check_password('password'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_registration_existing_email(self):
        url = reverse('registration')
        data = {
            'email': 'existing@example.com',
            'password': 'password',
            'gender': 'M',
            'date_of_birth': '1990-01-01',
            'weight': 70,
            'height': 180.5,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Email already exists')

    def test_registration_missing_data(self):
        url = reverse('registration')
        data = {
            'email': 'test@example.com',
            'password': 'password',
            'gender': 'M',
            'date_of_birth': '1990-01-01',
            'height': 180.5,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid registration data')


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password',
            gender='M',
            date_of_birth='1990-01-01',
            weight=70,
            height=180.5,
        )

    def test_login_success(self):
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'password',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_login_failure(self):
        url = reverse('login')
        data = {
            'email': 'chuj@gaga.com',
            'password': 'wrong_password',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access_token', response.data)
        self.assertNotIn('refresh_token', response.data)


class GetUserDataTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password',
            gender='M',
            date_of_birth='1990-01-01',
            weight=70,
            height=180.5,
        )
        
    def test_get_user_data_valid(self):
        url_login = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'password',
        }

        response = self.client.post(url_login, data, format='json')

        access_token = response.data['access_token']

        auth_string = 'Bearer' + ' ' + access_token
        get_data_header = {'Authorization': auth_string}

        url_get_data = reverse('get_user_data')

        response = self.client.get(url_get_data, headers=get_data_header, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], 'test@example.com')




class TokenLogicTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password',
            gender='M',
            date_of_birth='1990-01-01',
            weight=70,
            height=180.5,
        )

    def test_get_user_from_token(self):
        url_login = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'password',
        }

        response = self.client.post(url_login, data, format='json')

        access_token = response.data['access_token']

        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])

        user = get_user_from_token(access_token)

        self.assertIsNotNone(user)
        self.assertEqual(user.email, data['email'])










