# Generated by Django 5.1.2 on 2025-02-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BankDetail",
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
                ("account_number", models.CharField(max_length=20)),
                ("bank_name", models.CharField(max_length=100)),
                ("routing_code", models.CharField(max_length=11)),
                ("branch_name", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
