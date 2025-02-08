from django.db import models
class Timesheet(models.Model):
    timesheet_id = models.AutoField(primary_key=True)
    customer_name = models.ForeignKey('hra_customers.Customer', related_name='timesheets', on_delete=models.CASCADE)
    user_name = models.ForeignKey('hra_users.User', related_name='timesheets', on_delete=models.CASCADE)
    week_month = models.CharField(max_length=20)
    salary_mode = models.CharField(max_length=50)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    timesheet_status = models.CharField(max_length=50)
    attachment = models.FileField(upload_to='timesheet_attachments/', null=True, blank=True)

    def __str__(self):
        return f"Timesheet {self.timesheet_id} for {self.user_name}"

    class Meta:
        db_table = 'timesheet'
        verbose_name = 'Timesheet'
        verbose_name_plural = 'Timesheets'
