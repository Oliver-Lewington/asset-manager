# Generated by Django 5.1.4 on 2025-01-02 15:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_remove_maintenancehistory_status_after'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='AssignmentHistory',
        ),
    ]
