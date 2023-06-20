from django.urls import path

from . import views

urlpatterns = [
    path('add_meal/', views.AddMealView.as_view(), name='add_meal'),
    path('add_product_to_meal/', views.AddProductToMeal.as_view(), name='add_product_to_meal'),
    path('remove_product_from_meal/', views.RemoveProductFromMeal.as_view(), name='remove_product_from_meal'),

]