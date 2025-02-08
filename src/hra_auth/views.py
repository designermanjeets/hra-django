from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'hrkinfotech'
TOKEN_EXPIRATION_TIME = 30  # Token expiration time in minutes
REFRESH_TOKEN_EXPIRATION_TIME = 7  # Refresh token expiration time in days

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate access token
            access_token = generate_access_token(user)

            # Generate refresh token
            refresh_token = generate_refresh_token(user)

            # Set access token and refresh token as cookies
            response = JsonResponse({'message': 'Login successful'})
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True)

            return response
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def forget_password_view(request):
    if request.method == 'POST':
        # Logic for resetting password
        return JsonResponse({'message': 'Password reset successful'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        # Logic for user registration
        return JsonResponse({'message': 'User registered successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def generate_access_token(user):
    # Set token expiration time
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME)

    # Create payload for access token
    payload = {
        'user_id': user.id,
        'exp': expiration_time
    }

    # Generate access token
    access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return access_token

def generate_refresh_token(user):
    # Set token expiration time
    expiration_time = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION_TIME)

    # Create payload for refresh token
    payload = {
        'user_id': user.id,
        'exp': expiration_time
    }

    # Generate refresh token
    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return refresh_token
