from django.db import models
class Timesheet(models.Model):
    timesheet_id = models.AutoField(primary_key=True)
    purchase_order_id = models.ForeignKey('hra_purchase_orders.PurchaseOrder', related_name='purchase_order', on_delete=models.CASCADE,default=1)
    user_name = models.ForeignKey('hra_users.User', related_name='timesheets', on_delete=models.CASCADE)
    week_month = models.CharField(max_length=20)
    salary_mode = models.CharField(max_length=50)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    tenant_id = models.ForeignKey('hra_tenants.Tenant', on_delete=models.CASCADE,related_name='%(class)s_tenant_id',default=1)
    status = models.CharField(max_length=20,default='1') # 1=pending, 2=approved, 3=rejected
    image = models.TextField(default='')
    timesheet_detail = models.TextField(default='')
    def __str__(self):
        return f"Timesheet {self.timesheet_id} for {self.user_name}"
    class Meta:
        db_table = 'timesheet'
        verbose_name = 'Timesheet'
        verbose_name_plural = 'Timesheets'

