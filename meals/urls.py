from django.urls import path

from . import views

urlpatterns = [
    path('meal/', views.AddMealView.as_view(), name='add_meal'),
    path('add-product/', views.AddProductToMeal.as_view(), name='add_product_to_meal'),
    path('remove-product/', views.RemoveProductFromMeal.as_view(), name='remove_product_from_meal'),
    path('with-title/', views.GetProductsByTitle.as_view(), name='get_products_by_title'),
    path('product/', views.GetProduct.as_view(), name='product'),
]