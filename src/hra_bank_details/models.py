from django.db import models

# Create your models here.

class BankDetail(models.Model):
    user = models.ForeignKey('hra_users.User', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=100)
    routing_code = models.CharField(max_length=11)
    branch_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)