from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Permission

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    username = models.CharField(max_length=150, unique=True, default='username')
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, default='')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    job_role = models.CharField(max_length=100, default='emp')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    subscription = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenant_id = models.ForeignKey('hra_tenants.Tenant', on_delete=models.CASCADE,related_name='tenant_id')
    password = models.CharField(max_length=128, default='password')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    status = models.CharField(max_length=10,default='1')
    comment = models.TextField(default='')
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    def has_permission(self, perm_codename):
        if self.role:
            return self.role.permissions.filter(codename=perm_codename).exists()
        return False

    def __str__(self):
        return f"{self.user.username} - {self.role.name if self.role else 'No Role'}"



class EmpDetail(models.Model):
    user = models.ForeignKey("hra_users.User", on_delete=models.CASCADE,db_column='user_id',related_name='%(class)s_user_id')
    emp_code = models.CharField(max_length=20,unique=True,default="EMP001")
    joining_date = models.DateTimeField()
    dob = models.CharField(max_length=20)
    reporting_manager = models.ForeignKey("hra_users.User", on_delete=models.CASCADE,db_column='reporting_manager',related_name='%(class)s_reporting_manager')
    status = models.CharField(max_length=20,default ='1')
    class Meta:
        db_table = 'emp_detail'
    


class AddressDetail(models.Model):
    current_street_address_1 = models.CharField(max_length=100)
    current_street_address_2 = models.CharField(max_length=100, blank=True, null=True)
    current_country = models.CharField(max_length=100)
    current_state = models.CharField(max_length=20)
    current_city = models.CharField(max_length=100)
    current_zip_code = models.CharField(max_length=10)
    permanent_street_address_1 = models.CharField(max_length=100)
    permanent_street_address_2 = models.CharField(max_length=100, blank=True, null=True)
    permanent_country = models.CharField(max_length=100,blank=True)
    permanent_state = models.CharField(max_length=20,blank=True)
    permanent_city = models.CharField(max_length=100,blank=True)
    permanent_zip_code = models.CharField(max_length=10,blank=True)
    emp_id = models.ForeignKey("EmpDetail", on_delete=models.CASCADE,db_column='emp_id',default=1)

    def __str__(self):
        return self.street
    class Meta:
        db_table = 'address_model'


class PersonalDetail(models.Model):
    emp_id = models.ForeignKey("EmpDetail", on_delete=models.CASCADE,db_column='emp_id')
    ssn_number = models.CharField(max_length=100)
    home_phone = models.CharField(max_length=100)
    personal_number = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=100)
    status = models.CharField(max_length=10,default='1')

    class Meta:
        db_table= 'personal_detail'

class Visadetail(models.Model):
    emp_id = models.ForeignKey("EmpDetail", on_delete=models.CASCADE,db_column='emp_id')
    passport_number = models.CharField(max_length=100)
    passport_country = models.CharField(max_length=100)
    visa_type = models.CharField(max_length=100)
    visa_start_date= models.DateTimeField()
    visa_end_date = models.DateTimeField()
    visa_country = models.CharField(max_length=100)
    visa_renewal_date  = models.DateTimeField()
    visa_status = models.CharField(max_length=100)
    status = models.CharField(max_length=10,default='1')

    class Meta:
        db_table = 'visa_detail'


class Education(models.Model):
    emp_id = models.ForeignKey("EmpDetail", on_delete=models.CASCADE,db_column='emp_id')
    education = models.CharField(max_length=200)
    board = models.CharField(max_length=250)
    from_year = models.DateTimeField()
    to_year = models.DateTimeField()
    percentage = models.CharField(max_length=20)
    school = models.CharField(max_length=200)
    edu_type = models.CharField(max_length=100)
    status = models.CharField(max_length=10,default='1')
    class Meta:
        db_table = "education_model"

class Experience(models.Model):
    emp_id = models.ForeignKey("EmpDetail", on_delete=models.CASCADE,db_column='emp_id')
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True)
    salary_mode = models.CharField(max_length=20,default='Hourly')
    hourly_rate  = models.CharField(max_length=20)
    skills = models.TextField()
    status = models.CharField(max_length=10,default='1')
    class Meta:
        db_table = "experience_model"






