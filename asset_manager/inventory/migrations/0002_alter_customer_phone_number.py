# Generated by Django 5.1.4 on 2024-12-18 20:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=20, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must start with an optional '+' followed by digits, with optional spaces.", regex='^\\+?[\\d\\s]+$')]),
        ),
    ]
