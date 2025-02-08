from django.db import models

class User(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    job_role = models.CharField(max_length=100)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    subscription = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenant_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"