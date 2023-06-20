from rest_framework import serializers
from .models import Product, Meal, MealElement


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'measure_type', 'kcal', 'isVerified']

class MealElementSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = MealElement
        fields = ['product', 'quantity']

class MealSerializer(serializers.ModelSerializer):
    product_list = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'title', 'calories', 'creation_date', 'product_list']

    # def get_elements(self, obj):
    #     return obj.mealelement_set.all()

