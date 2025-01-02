from django import forms
from ..models import Asset

class AssetForm(forms.ModelForm):
    """
    A unified form for creating and updating assets with consistent behavior and styling.
    """
    class Meta:
        model = Asset
        fields = ['name', 'assigned_to', 'warranty_expiry', 'status', 'description']

    # Define form fields with custom attributes directly
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter asset name',
        }),
        label='Asset Name',
        max_length=255,
        required=True
    )
    warranty_expiry = forms.DateField(
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'Select a warranty expiry date',
        }),
        label='Warranty Expiry Date (Optional)',
        required=False
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Enter asset description...',
        }),
        label='Description (Optional)',
        required=False
    )
