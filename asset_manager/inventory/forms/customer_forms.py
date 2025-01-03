from django import forms
from ..models import Customer

class CustomerForm(forms.ModelForm):
    """
    A unified form for creating and updating customers with consistent behavior and styling.
    """
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'email']

    # Define form fields with custom attributes directly
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter customer name',
        }),
        label='Customer Name',
        max_length=200,
        required=True
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number',
        }),
        label='Phone Number',
        max_length=20,
        required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address',
        }),
        label='Email Address',
        max_length=200,
        required=True
    )
