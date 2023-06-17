from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from .models import User
import json
import jwt

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate


class RegistrationView(APIView):
    def post(self, request):

        if User.objects.filter(email=request.data.get('email')).exists():
            return Response({'error': 'Email already exists'}, status=400)

        try:
            User.objects.create_user(
                email=request.data.get('email'),
                password=request.data.get('password'),
                gender=request.data.get('gender'),
                date_of_birth=request.data.get('date_of_birth'),
                weight=request.data.get('weight'),
                height=request.data.get('height')
            )
        except:
            return Response({'error': 'Invalid registration data'}, status=400)

        return Response({'message': 'Registration successful!'}, status=200)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=400)

@api_view()
def index(request):
    return Response({'message': "Hello, world. You're at the accounts index."})
