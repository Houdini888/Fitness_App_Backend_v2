from django.db import models
from enum import Enum


from django.contrib.auth import get_user_model
User = get_user_model()

class MeasureType(Enum):
    HundrGrams = '100g'
    HundrMilis = '100ml'
    Teaspoon = 'tsp'
    Tablespoon = 'tbsp'
    Glass = 'glass'

class Product(models.Model):

    title = models.CharField(max_length=100)

    MEASURE_CHOICES = [(MeasureType.HundrGrams.value, MeasureType.HundrGrams.name),
                       (MeasureType.HundrMilis.value, MeasureType.HundrMilis.name),
                       (MeasureType.Teaspoon.value, MeasureType.Teaspoon.name),
                       (MeasureType.Tablespoon.value, MeasureType.Tablespoon.name),
                       (MeasureType.Glass.value, MeasureType.Glass.name),
                       ]
    measure_type = models.CharField(choices=MEASURE_CHOICES, max_length=10)

    kcal = models.IntegerField()
    isVerified = models.BooleanField()
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Meal(models.Model):

    title = models.CharField(unique=True, max_length=255)
    subtitle = models.TextField()
    calories = models.IntegerField

    creation_date = models.DateField
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE)

    product_list = models.ManyToManyField(Product, through='MealElement')


class MealElement(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    quantity = models.IntegerField()

