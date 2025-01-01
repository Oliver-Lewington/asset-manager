from django import forms
from .models import Asset, MaintenanceHistory


class MaintenanceHistoryForm(forms.ModelForm):
    class Meta:
        model = MaintenanceHistory
        fields = ['maintenance_type', 'description', 'status_after']




