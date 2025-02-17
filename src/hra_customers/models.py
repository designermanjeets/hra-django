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
    tenant_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_display_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    other = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    notes = models.TextField()
    contact_person_salutation = models.CharField(max_length=100)
    contact_person_first_name = models.CharField(max_length=100)
    contact_person_middle_name = models.CharField(max_length=100)
    contact_person_last_name = models.CharField(max_length=100)
    contact_person_email = models.CharField(max_length=100)
    contact_person_work_phone = models.CharField(max_length=100)
    contact_person_mobile_no = models.CharField(max_length=100)
    
    
    

    def __str__(self):
        return self.customer_name
    
    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'