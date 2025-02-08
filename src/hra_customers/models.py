from django.db import models
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    billing_address = models.ForeignKey('hra_address.Address', related_name='billing_address', on_delete=models.CASCADE)
    shipping_address = models.ForeignKey('hra_address.Address', related_name='shipping_address', on_delete=models.CASCADE)
    billing_cycle = models.CharField(max_length=50)
    payment_terms = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=100)
    tenant_id = models.CharField(max_length=100)

    def __str__(self):
        return self.customer_name
    
    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'