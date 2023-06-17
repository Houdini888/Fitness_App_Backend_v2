import json

from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse
from accounts.custom_backend import CustomBackend
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate
#from .models import User

from rest_framework import status
from rest_framework.test import APIClient

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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(email='test@example.com').email, 'test@example.com')
        self.assertTrue(User.objects.get(email='test@example.com').check_password('password'))

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









