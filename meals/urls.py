from django.urls import path

from . import views

urlpatterns = [
    path('add_meal/', views.AddMealView.as_view(), name='add_meal'),

]