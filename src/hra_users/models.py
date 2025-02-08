from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    username = models.CharField(max_length=150, unique=True, default='username')
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, default='')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    job_role = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    subscription = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenant_id = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=128, default='password')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"