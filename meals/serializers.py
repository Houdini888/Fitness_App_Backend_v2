from rest_framework import serializers
from .models import Product, Meal, MealElement


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'measure_type', 'kcal', 'isVerified']


class ProductSerializer_WithQuantity(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'creator_user', 'quantity',  'title', 'measure_type', 'kcal', 'isVerified']

    def get_quantity(self, instance):
        meal_element = MealElement.objects.filter(product=instance).first()
        return meal_element.quantity


class MealElementSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = MealElement
        fields = ['product', 'quantity']

class MealSerializerProductList(serializers.ModelSerializer):
    product_list = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'title', 'calories', 'creation_date', 'product_list']

class MealSerializerProductList_WithQuantity(serializers.ModelSerializer):
    product_list = ProductSerializer_WithQuantity(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'title', 'calories', 'creation_date', 'product_list']





