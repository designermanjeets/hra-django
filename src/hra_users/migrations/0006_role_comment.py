# Generated by Django 5.1.2 on 2025-02-19 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hra_users", "0005_role_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="role",
            name="comment",
            field=models.TextField(default=""),
        ),
    ]
