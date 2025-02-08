from django.db import models

class ReportingManager(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.ForeignKey('hra_address.Address', on_delete=models.CASCADE)
    tenant_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'reporting_manager'
        verbose_name = 'Reporting Manager'
        verbose_name_plural = 'Reporting Managers'
