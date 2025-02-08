# Generated by Django 5.1.2 on 2025-02-08 12:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("hra_customers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PurchaseOrder",
            fields=[
                (
                    "purchase_order_id",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("po_name", models.CharField(max_length=100)),
                (
                    "hourly_rate",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("status", models.CharField(max_length=50)),
                ("tenant_id", models.CharField(max_length=100)),
                (
                    "customer_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchase_orders",
                        to="hra_customers.customer",
                    ),
                ),
            ],
            options={
                "verbose_name": "Purchase Order",
                "verbose_name_plural": "Purchase Orders",
                "db_table": "purchase_order",
            },
        ),
    ]
