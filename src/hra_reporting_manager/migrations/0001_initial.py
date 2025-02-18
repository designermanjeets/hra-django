# Generated by Django 5.1.2 on 2025-02-17 14:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("hra_address", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReportingManager",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=15)),
                ("tenant_id", models.CharField(max_length=100)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hra_address.address",
                    ),
                ),
            ],
            options={
                "verbose_name": "Reporting Manager",
                "verbose_name_plural": "Reporting Managers",
                "db_table": "reporting_manager",
            },
        ),
    ]
