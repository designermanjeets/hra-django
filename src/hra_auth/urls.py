from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view),
    path('forget-password/', views.forget_password_view),
    path('signup/', views.signup_view),
]