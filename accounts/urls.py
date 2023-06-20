from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user-data/', views.GetUserData.as_view(), name='get_user_data'),
    path('password/', views.ChangePasswordView.as_view(), name='change_password')
]