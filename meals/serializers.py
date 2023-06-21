from rest_framework import serializers
from .models import Product, Meal, MealElement


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'measure_type', 'kcal', 'isVerified', 'creator_user']


class ProductSerializer_WithElementData(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
    meal_element_id = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'meal_element_id', 'creator_user', 'quantity',  'title', 'measure_type', 'kcal', 'isVerified']

    def get_quantity(self, instance):
        meal_element = MealElement.objects.filter(product=instance).first()
        return meal_element.quantity
    def get_meal_element_id(self, instance):
        meal_element = MealElement.objects.filter(product=instance).first()
        return meal_element.id


class MealElementSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = MealElement
        fields = ['product', 'quantity']

class MealSerializerProductList(serializers.ModelSerializer):
    product_list = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'title', 'creation_date', 'product_list']

class MealSerializerProductList_WithQuantity(serializers.ModelSerializer):
    product_list = ProductSerializer_WithElementData(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'title', 'creation_date', 'product_list']





