from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.token_logic import authenticate_user_from_request

from .models import Product, Meal, MealElement

from datetime import date
import json

from django.contrib.auth import get_user_model

User = get_user_model()


# add a meal with all initial products
class AddMealView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = authenticate_user_from_request(request)

        if user:
            try:
                meal = Meal.objects.create(
                    title=request.data.get('title'),
                    subtitle=request.data.get('subtitle'),
                    calories=request.data.get('calories'),
                    creation_date=date.today(),
                    creator_user=user,
                )
            except:
                return Response({'error': 'Invalid meal data'}, status=400)

            # products_id_quant_list is a list of dicts with keys {product_id, quantity}
            products_id_quant_list = request.data.get('products')

            for product_id_quant in products_id_quant_list:
                prod_id = product_id_quant['product_id']
                product = Product.objects.get(id=prod_id)

                if product:
                    MealElement.objects.create(
                        product=product,
                        meal=meal,
                        quantity=product_id_quant['quantity']
                    )
                else:
                    return Response({'error': f'Invalid product id: {prod_id}'}, status=400)

        else:
            return Response({'error': 'Invalid token'}, status=400)

        return Response({'message': 'Meal added successfully', 'meal_id': meal.id})


# get request with meal_id, product_id and quantity and add product to meal's product_list
class AddProductToMeal(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = authenticate_user_from_request(request)

        if user:
            try:
                meal_id = request.data.get('meal_id')
                product_id = request.data.get('product_id')
                quantity = request.data.get('quantity')

                meal = Meal.objects.get(id=meal_id)
                product = Product.objects.get(id=product_id)

                MealElement.objects.create(product=product, meal=meal, quantity=quantity)
            except:
                return Response({'error': 'Invalid meal or product data'}, status=400)

            return Response({'message': 'Product successfully added to meal'})


# get request with meal_id and product_id, then remove product from meal
class RemoveProductFromMeal(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = authenticate_user_from_request(request)

        if user:
            try:
                meal_id = request.data.get('meal_id')
                product_id = request.data.get('product_id')

                meal = Meal.objects.get(id=meal_id)
                product = Product.objects.get(id=product_id)

                elements_to_delete = MealElement.objects.filter(meal=meal, product=product)
                elements_to_delete.delete()
            except:
                return Response({'error': 'Invalid meal or product data'}, status=400)

        return Response({'message': 'Product successfully removed from meal'})
