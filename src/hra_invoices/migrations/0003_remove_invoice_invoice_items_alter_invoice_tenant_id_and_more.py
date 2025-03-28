# Generated by Django 5.1.2 on 2025-02-27 13:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hra_invoices', '0002_initial'),
        ('hra_tenants', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='invoice_items',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tenant_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_tenant_id', to='hra_tenants.tenant'),
        ),
        migrations.DeleteModel(
            name='InvoiceItem',
        ),
    ]
