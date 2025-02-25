from django.db import models

# Create your models here.
class Address(models.Model):
    current_street_address_1 = models.CharField(max_length=100)
    current_street_address_2 = models.CharField(max_length=100, blank=True, null=True)
    current_country = models.CharField(max_length=100)
    current_state = models.CharField(max_length=20)
    current_city = models.CharField(max_length=100)
    current_zip_code = models.CharField(max_length=10)
    # permanent_street_address_1 = models.CharField(max_length=100)
    # permanent_street_address_2 = models.CharField(max_length=100, blank=True, null=True)
    # permanent_country = models.CharField(max_length=100)
    # permanent_state = models.CharField(max_length=20)
    # permanent_city = models.CharField(max_length=100)
    # permanent_zip_code = models.CharField(max_length=10)
    # tenant = models.ForeignKey("hra_tenants.Tenant", on_delete=models.CASCADE, related_name='addresses')
    # user = models.ForeignKey("hra_users.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.street