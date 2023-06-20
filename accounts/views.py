from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .token_logic import authenticate_user_from_request

from django.contrib.auth import authenticate

from .serializers import UserSerializer

# from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):

        if User.objects.filter(email=request.data.get('email')).exists():
            return Response({'error': 'Email already exists'}, status=400)

        try:
            user = User.objects.create_user(
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


class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            user = authenticate_user_from_request(request)

            if user:
                old_password = request.data.get('old_password')
                new_password = request.data.get('new_password')

                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password changed successfully'})
                else:
                    return Response({'error': 'The old password is incorrect!'}, status=400)
        except:
            return Response({'error': 'User authentication failed'}, status=400)


class GetUserData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = authenticate_user_from_request(request)

            if user:
                serializer = UserSerializer(user)
                user_data = serializer.data
                return Response(user_data)
            else:
                return Response({'error': 'User not found'})

        except:
            return Response({'error': 'Authentication failed'})


class UpdateUserData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    allowed_methods = ['PATCH']
    def patch(self, request):
        try:
            user_email = authenticate_user_from_request(request)

            if not user_email:
                return Response({'error': 'Invalid token'})

            user = User.objects.get(email=user_email)

            user.update_details(
                gender=request.data.get('gender', user.gender),
                date_of_birth=request.data.get('date_of_birth', user.date_of_birth),
                weight=request.data.get('weight', user.weight),
                height=request.data.get('height', user.height)
            )
            user.save()
        except Exception as error:
            print(error)
            return Response({'error': 'Bad request'}, 400)

        return Response()


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
