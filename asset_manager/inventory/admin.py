from django.contrib import admin
from .models import Customer, Asset, AssignmentHistory, MaintenanceHistory

# Register your models here.
admin.site.register(Customer)
admin.site.register(Asset)
admin.site.register(AssignmentHistory)
admin.site.register(MaintenanceHistory)