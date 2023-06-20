from rest_framework import serializers
from .models import Product, Meal, MealElement


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'measure_type', 'kcal', 'isVerified']