from django.db import models

class PurchaseOrder(models.Model):
    purchase_order_id = models.AutoField(primary_key=True)
    po_name = models.CharField(max_length=100)
    #assigned_to = models.ForeignKey('hra_users.User', related_name='hra_users', on_delete=models.CASCADE, null=True)
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


class AssignPurchaseOrder(models.Model):
    tenant_id = models.ForeignKey('hra_tenants.Tenant', on_delete=models.CASCADE,related_name='%(class)s_tenant_id',default=1)
    purchase_order_id = models.ForeignKey('PurchaseOrder', related_name='%(class)s_purchase_order_id', on_delete=models.CASCADE)
    user_id = models.ForeignKey('hra_users.User', related_name='%(class)s_user_id', on_delete=models.CASCADE)
    status = models.CharField(max_length=50,default="1")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.purchase_order_id

    class Meta:
        db_table = 'assign_purchase_order'
        verbose_name = 'Assign Purchase Order'
        verbose_name_plural = 'Assign Purchase Orders'





