# Generated by Django 5.0.6 on 2025-03-12 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hra_users', '0013_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='empdetail',
            name='hourly_rate',
            field=models.CharField(default='5', max_length=20),
        ),
        migrations.AddField(
            model_name='empdetail',
            name='salary_mode',
            field=models.CharField(default='Hourly', max_length=20),
        ),
    ]
