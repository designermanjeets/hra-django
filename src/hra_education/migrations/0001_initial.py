# Generated by Django 5.1.2 on 2025-02-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Education",
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
                ("education_type", models.CharField(max_length=100)),
                ("college", models.CharField(max_length=100)),
                ("year_of_passing", models.DateField()),
                ("major_specialization", models.CharField(max_length=100)),
                ("tenant_id", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Education",
                "verbose_name_plural": "Educations",
                "db_table": "education",
            },
        ),
    ]
