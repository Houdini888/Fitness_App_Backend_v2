from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.token_logic import authenticate_user_from_token

from .models import Product, Meal, MealElement

from datetime import date
import json

from django.contrib.auth import get_user_model
User = get_user_model()

#add a meal with all initial products
class AddMealView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):


            user = authenticate_user_from_token(request)

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


                #products_id_quant_list is a list of dicts with keys {product_id, quantity}
                products_id_quant_list = request.data.get('products')

                for product_id_quant in products_id_quant_list:
                    product = Product.objects.get(id=product_id_quant['product_id'])

                    if product:
                        MealElement.objects.create(
                            product=product,
                            meal=meal,
                            quantity=product_id_quant['quantity']
                        )
                    else:
                        return Response({'error': 'Invalid product'}, status=400)

            else:
                return Response({'error': 'User authentication failed'}, status=400)

            return Response({'message': 'Meal added successfully'})


