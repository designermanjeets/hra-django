# Generated by Django 5.1.2 on 2025-02-25 19:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "hra_purchase_orders",
            "0003_remove_purchaseorder_assigned_to_assignpurchaseorder",
        ),
        ("hra_tenants", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="assignpurchaseorder",
            name="tenant_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_tenant_id",
                to="hra_tenants.tenant",
            ),
        ),
        migrations.AlterField(
            model_name="assignpurchaseorder",
            name="purchase_order_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_purchase_order_id",
                to="hra_purchase_orders.purchaseorder",
            ),
        ),
        migrations.AlterField(
            model_name="assignpurchaseorder",
            name="status",
            field=models.CharField(default="1", max_length=50),
        ),
        migrations.AlterField(
            model_name="assignpurchaseorder",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_user_id",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
