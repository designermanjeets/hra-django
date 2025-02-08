from django.db import models

class Education(models.Model):
    user = models.ForeignKey('hra_users.User', on_delete=models.CASCADE)
    education_type = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    year_of_passing = models.DateField()
    major_specialization = models.CharField(max_length=100)
    tenant_id = models.CharField(max_length=100)

    def __str__(self):
        return self.degree
    
    class Meta:
        db_table = 'education'
        verbose_name = 'Education'
        verbose_name_plural = 'Educations'

