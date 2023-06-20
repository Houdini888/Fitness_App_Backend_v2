from django.test import TestCase

import json
import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.test import APIClient

from accounts.token_logic import get_user_from_token

from .models import Product, Meal, MealElement

from django.contrib.auth import get_user_model

User = get_user_model()


class AddMealViewTest(TestCase):
    # def setUp(self):
        # self.client = APIClient()
        # self.product1 = Product.objects.create(
        #     title='Product1',
        #     measure_type='100g',
        #     kcal=300,
        #     isVerified=True,
        # )
        # self.product2 = Product.objects.create(
        #     title='Product2',
        #     measure_type='100g',
        #     kcal=500,
        #     isVerified=True,
        # )

    def test_add_meal_success(self):

        url = reverse('add_meal')

        data = {
                  "title": "Meal Title",
                  "subtitle": "Meal Subtitle",
                  "calories": 500,
                  "products": [
                    {
                      "product_id": 1,
                      "quantity": 2
                    },
                    {
                      "product_id": 2,
                      "quantity": 3
                    }
                  ]
                }

        try:

            products_json = data['products']
            # products_id_quant_list is a list of dicts with keys {product_id, quantity}
            products_id_quant_list = data['products']
        except Exception as e:
            print(str(e))

        for product in products_id_quant_list:
            print(product)

