from django.db import models

class Experience(models.Model):
    customer_name = models.CharField(max_length=255)
    project_start_date = models.DateField()
    project_end_date = models.DateField()
    billing_type = models.CharField(max_length=50)
    billing_rate = models.DecimalField(max_digits=10, decimal_places=2)
    skills = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_name
    
    class Meta:
        db_table = 'experience'
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'
