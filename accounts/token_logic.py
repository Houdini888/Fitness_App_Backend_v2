import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

def get_token_from_header(request):
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            return token
        else:
            raise AuthenticationFailed('Invalid token format')
    except Exception as e:
        raise AuthenticationFailed('Failed to retrieve token from header') from e


def get_user_from_token(token) -> User:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token['user_id']
        # Retrieve the user object using the user_id
        user = User.objects.get(id=user_id)
        return user
    except (jwt.DecodeError, User.DoesNotExist):
        return None

def authenticate_user_from_token(request) -> User:
    token = get_token_from_header(request)
    user = get_user_from_token(token)

    if user:
        return user
    else:
        raise AuthenticationFailed('User authentication failed')
