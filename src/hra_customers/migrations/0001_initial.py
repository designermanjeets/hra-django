# Generated by Django 5.1.2 on 2025-02-17 14:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("hra_address", "0001_initial"),
        ("hra_tenants", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "customer_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("customer_name", models.CharField(max_length=100)),
                ("company_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.CharField(max_length=15)),
                ("billing_cycle", models.CharField(max_length=50, null=True)),
                ("payment_terms", models.CharField(max_length=50, null=True)),
                ("title", models.CharField(max_length=255, null=True)),
                ("first_name", models.CharField(max_length=100, null=True)),
                ("middle_name", models.CharField(max_length=100, null=True)),
                ("last_name", models.CharField(max_length=100, null=True)),
                (
                    "company_display_name",
                    models.CharField(max_length=100, null=True),
                ),
                ("mobile_number", models.CharField(max_length=100, null=True)),
                ("fax", models.CharField(max_length=100, null=True)),
                ("other", models.CharField(max_length=100, null=True)),
                ("website", models.CharField(max_length=100, null=True)),
                ("notes", models.TextField(null=True)),
                (
                    "contact_person_salutation",
                    models.CharField(max_length=100, null=True),
                ),
                (
                    "contact_person_first_name",
                    models.CharField(max_length=100, null=True),
                ),
                (
                    "contact_person_middle_name",
                    models.CharField(max_length=100, null=True),
                ),
                (
                    "contact_person_last_name",
                    models.CharField(max_length=100, null=True),
                ),
                (
                    "contact_person_email",
                    models.CharField(max_length=100, null=True),
                ),
                (
                    "contact_person_work_phone",
                    models.CharField(max_length=100, null=True),
                ),
                (
                    "contact_person_mobile_no",
                    models.CharField(max_length=100, null=True),
                ),
                ("status", models.CharField(default="1", max_length=100)),
                (
                    "billing_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="billing_address",
                        to="hra_address.address",
                    ),
                ),
                (
                    "shipping_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shipping_address",
                        to="hra_address.address",
                    ),
                ),
                (
                    "tenant_id",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hra_tenants.tenant",
                    ),
                ),
            ],
            options={
                "verbose_name": "Customer",
                "verbose_name_plural": "Customers",
                "db_table": "customer",
            },
        ),
    ]
