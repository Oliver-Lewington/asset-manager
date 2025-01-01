from django import forms
from ..models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'description', 'warranty_expiry', 'status']
        
# - Create an Asset
class CreateAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'warranty_expiry', 'status', 'description']
        widgets = {
            'warranty_expiry': forms.TextInput(attrs={
                'class': 'form-control datepicker', 
                'placeholder': 'Select a date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Add a description...'
            }),
        }

# - Update an Asset
class UpdateAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'warranty_expiry', 'status', 'description']
        widgets = {
            'warranty_expiry': forms.TextInput(attrs={
                'class': 'form-control datepicker', 
                'placeholder': 'Select a date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Update the description...'
            }),
        }