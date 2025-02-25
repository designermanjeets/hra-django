from django.db import models


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    billing_address = models.ForeignKey('hra_address.Address', related_name='billing_address', on_delete=models.CASCADE)
    shipping_address = models.ForeignKey('hra_address.Address', related_name='shipping_address', on_delete=models.CASCADE)
    billing_cycle = models.CharField(max_length=50,null=True)
    payment_terms = models.CharField(max_length=50,null=True)
    tenant_id = models.ForeignKey('hra_tenants.Tenant', on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=255,null=True)
    first_name = models.CharField(max_length=100,null=True)
    middle_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    company_display_name = models.CharField(max_length=100,null=True)
    mobile_number = models.CharField(max_length=100,null=True)
    fax = models.CharField(max_length=100,null=True)
    other = models.CharField(max_length=100,null=True)
    website = models.CharField(max_length=100,null=True)
    notes = models.TextField(null=True)
    contact_person_salutation = models.CharField(max_length=100,null=True)
    contact_person_first_name = models.CharField(max_length=100,null = True)
    contact_person_middle_name = models.CharField(max_length=100,null=True)
    contact_person_last_name = models.CharField(max_length=100,null=True)
    contact_person_email = models.CharField(max_length=100,null=True)
    contact_person_work_phone = models.CharField(max_length=100,null=True)
    contact_person_mobile_no = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=100,default='1')

    

    def __str__(self):
        return self.customer_name
    
    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'