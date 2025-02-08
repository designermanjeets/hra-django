from django.db import models

class Lookup(models.Model):
    category = models.CharField(max_length=255)
    config_key = models.CharField(max_length=255)
    config_value = models.CharField(max_length=255)
    tenant = models.ForeignKey('hra_tenants.Tenant', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.config_key}"
