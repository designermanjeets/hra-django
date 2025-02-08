from django.db import models

class PurchaseOrder(models.Model):
    purchase_order_id = models.AutoField(primary_key=True)
    po_name = models.CharField(max_length=100)
    assigned_to = models.ForeignKey('hra_users.User', related_name='hra_users', on_delete=models.CASCADE, null=True)
    customer_name = models.ForeignKey('hra_customers.Customer', related_name='purchase_orders', on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    tenant_id = models.CharField(max_length=100)

    def __str__(self):
        return self.po_name

    class Meta:
        db_table = 'purchase_order'
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
