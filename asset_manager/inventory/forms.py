# Create forms for users who want to register and login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput

from django import forms

# Register/Create a user

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2'] # Password 2 is a confirmation of their password
    
# - Login a user 
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput)


# # - Create a record
# class CreateRecordForm(forms.ModelForm):
#     class Meta:
#         model = Record
#         fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'county', 'country'] 

# # - Update a record
# class UpdateRecordForm(forms.ModelForm):
#     class Meta:
#         model = Record
#         fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'county', 'country'] 
