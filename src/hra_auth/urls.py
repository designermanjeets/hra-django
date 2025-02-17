from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.login_view),
    path('login', views.LoginView.as_view()),
    path('forgot-password', views.ForgotPassword.as_view()),
    path('verify-token', views.VerifyTokenAPIView.as_view()),
    path('change-password', views.ChangePassword.as_view()),
    
    # path('signup/', views.signup_view),
    path('signup', views.UserSignup.as_view()),
]