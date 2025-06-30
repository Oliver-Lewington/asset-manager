from django.contrib import admin
from .models import Customer, Asset, MaintenanceHistory

# Register your models here.
admin.site.register(Asset)
admin.site.register(Customer)
admin.site.register(MaintenanceHistory)