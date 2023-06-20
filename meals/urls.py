from django.urls import path

from . import views

urlpatterns = [
    path('meal/', views.AddMealView.as_view(), name='add_meal'),
    path('add-product-to-meal/', views.AddProductToMeal.as_view(), name='add_product_to_meal'),
    path('remove-product/', views.RemoveProductFromMeal.as_view(), name='remove_product_from_meal'),
    path('product-with-title/', views.GetProductsByTitle.as_view(), name='get_products_by_title'),
    path('product/', views.GetProduct.as_view(), name='product'),
    path('meals-in-range/', views.GetMealsBetweenDates.as_view(), name='meals-in-range'),
    path('get-meal/', views.GetMeal.as_view(), name='get-meal'),
    path('add-product/', views.AddProduct.as_view(), name='add-product'),
]
