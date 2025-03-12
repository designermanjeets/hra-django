from django.http import JsonResponse
# from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate ,login, logout
import jwt
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
import logging
import secrets
import string
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import jwt
import datetime
from jwt import ExpiredSignatureError, InvalidTokenError
from rest_framework_simplejwt.tokens import RefreshToken
from hra_users.models import *

# SECRET_KEY = "your_secret_key"
# logger = logging.getLogger(__name__)



SECRET_KEY = 'hrkinfotech'
TOKEN_EXPIRATION_TIME = 30  # Token expiration time in minutes
REFRESH_TOKEN_EXPIRATION_TIME = 7 
SENDER_EMAIL = "karanid420@gmail.com"  # Replace with your Gmail
SENDER_PASSWORD = "ruqv oyui xbkt ulok"  # Use an App Password for security

# Refresh token expiration time in days
from django.contrib.auth import get_user_model
User = get_user_model()





class LoginView(APIView):
    def post(self, request):
        print("Login API")
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            return Response({"Message": "Invalid request","status":False}, status=status.HTTP_400_BAD_REQUEST)
            
        print(username,password)
        user = authenticate(username=username, password=password)
        # logger.info()
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            user_profile = UserProfile.objects.get(user=user)
            user_role = user_profile.role.name if user_profile.role else "No Role"
            return  Response({'message': 'Login successful',"status":True,"access_token":access_token,"refresh_token":str(refresh),"role":user_role},status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials',"status":False}, status=status.HTTP_401_UNAUTHORIZED)

class ForgotPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        print(user,"user_test")
        if user:
            # Generate password reset token
            password_reset_token = generate_password_reset_token(user)
            # Send password reset email
            send_password_reset_email(user, password_reset_token)
            return Response({'message': 'Password reset email sent',"status":True}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found',"status":False}, status=status.HTTP_404_NOT_FOUND)
          
class VerifyTokenAPIView(APIView):
    def post(self, request):
        # Extract the token from the POST request data
        token = request.data.get("token")
        if not token:
            return Response(
                {"error": "Token is missing"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the token
        result = verify_password_reset_token(token)
        print(result,"result")
        if result.get("valid"):
            try:
                user = User.objects.get(email=result.get("email"), first_name=result.get("name"), phone_number=result.get("phone"))
            except User.DoesNotExist:
                return Response(
                    {"status": False, "error": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response({"status": True}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"status": False, "error": result.get("error")},
                status=status.HTTP_400_BAD_REQUEST
            )

class ChangePassword(APIView):
    def post(self, request):
        # Extract the token from the POST request data
        print(request.POST)
        token = request.data.get("token")
        new_password = request.data.get("password")
        data=verify_password_reset_token(token)
        print(data)
        if data.get("valid"):
            email=data.get("email")
            try:
                user = User.objects.filter(email=email).update(password=make_password(new_password))
                return Response({"message":"password Updated Succesfuly","status":True},status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Try again later","status":False}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Reset Password Link Expired","status":False}, status=status.HTTP_404_NOT_FOUND)

# Send password reset email using a library like django.core.mail
class UserSignup(APIView):
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        first_name=  request.data.get('first_name')
        last_name=  request.data.get('last_name')
        email=  request.data.get('email')
        # phone_number=  request.data.get('phone_number')
        gender=  request.data.get('gender')
        job_role=  request.data.get('job_role')
       
        # Create user
        
        user = User.objects.create_user(username=username,email=email, password=password,phone_number=phone_number,first_name=first_name,last_name=last_name,gender=gender,job_role=job_role )
            
        print(user)
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        # access_token = ""
        # refresh_token = ""
        # print("User created successfully",user)
        response = JsonResponse({'message': 'User created successfully', 'access_token': access_token, 'refresh_token': refresh_token,"status_key":True})
        
        
        return response
        # return JsonResponse({'message': 'User registered successfully'})

def generate_access_token(user):
    # Set token expiration time
    expiration_time = datetime.datetime.now() + timedelta(minutes=TOKEN_EXPIRATION_TIME)

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
    expiration_time = datetime.datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRATION_TIME)

    # Create payload for refresh token
    payload = {
        'user_id': user.id,
        'exp': expiration_time
    }

    # Generate refresh token
    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return refresh_token

def generate_password_reset_token(user):
    payload = {
        "email": user.email,
        "name": user.first_name,
        "phone": user.phone_number,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_TIME)  # Token expires in 1 hour
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# def verify_password_reset_token(token):
#     if True:
#         if isinstance(token, str):
#             token = token.encode('utf-8')
#         print(type(token))
#         decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         print(decoded_payload)
#         return {
#             "email": decoded_payload["email"],
#             "name": decoded_payload["name"],
#             "phone": decoded_payload["phone"],
#             "valid": True
#         }
#     # except jwt.ExpiredSignatureError:
#     #     return {"error": "Token has expired", "valid": False}
#     # except jwt.InvalidTokenError:
#     #     return {"error": "Invalid token", "valid": False}


def verify_password_reset_token(token):
    # Check that a token was provided
    if not token:
        return {"valid": False, "error": "No token provided"}
    
    # Ensure token is a string before encoding to bytes
    if isinstance(token, str):
        token = token.encode('utf-8')
    
    print("Token type:", type(token))
    
    if True:
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("Decoded payload:", decoded_payload)
        return {
            "email": decoded_payload["email"],
            "name": decoded_payload["name"],
            "phone": decoded_payload["phone"],
            "valid": True
        }
    # except ExpiredSignatureError:
    #     return {"valid": False, "error": "Token has expired"}
    # except InvalidTokenError:
    #     return {"valid": False, "error": "Invalid token"}


def send_password_reset_email(user, password_reset_token):
    sender_email = SENDER_EMAIL  # Replace with your Gmail
    sender_password = SENDER_PASSWORD  # Use an App Password for security
    receiver_email = user.email  # Get user's email

    # Email subject & body
    subject = "Password Reset Request"
    body = f"""
    Hello {user.first_name},

    We received a request to reset your password. Click the link below to reset it:

    <a href="http://localhost:3001/reset-password?token={password_reset_token}">Reset-Password Link </a>

    If you did not request this, please ignore this email.

    Best,
    Your Website Team
    """

    # Create MIME Email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    # Establish a secure connection and send the email
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return "Mail sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"
 






