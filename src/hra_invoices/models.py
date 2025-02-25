from django.db import models

class InvoiceItem(models.Model):
    invoice = models.ForeignKey('Invoice', related_name='items', on_delete=models.CASCADE)  # Changed related_name to 'items'
    product_service = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.product_service} - {self.invoice.invoice_number}"
    class Meta:
        db_table = 'invoice_item'
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'



class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    customer_name = models.ForeignKey('hra_customers.Customer', related_name='customers', on_delete=models.CASCADE)
    purchase_order = models.ForeignKey('hra_purchase_orders.PurchaseOrder', related_name='purchase_orders', on_delete=models.CASCADE)
    invoice_number = models.IntegerField()
    order_number = models.IntegerField()
    invoice_date = models.DateField()
    due_date = models.DateField()
    terms = models.CharField(max_length=100)
    invoice_month = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=50)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    terms_and_condition = models.TextField()
    customer_notes = models.TextField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_status = models.CharField(max_length=50)
    tenant_id = models.CharField(max_length=100)
    invoice_items = models.ManyToManyField('InvoiceItem', related_name='invoices')
    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.customer_name}"
    class Meta:
        db_table = 'invoice'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
