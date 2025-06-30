from django import forms
from django.core.cache import cache
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    """
    Form to create a new user with optional admin privileges.
    """
    is_admin = forms.BooleanField(
        required=False,
        initial=False,
        label="Register as Administrator",
        help_text="Checking this box will grant you admin privileges, enabling you to add, edit and delete customer, asset and maintenance records.",
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_admin']
        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        widgets = {
            'username': TextInput(attrs={'placeholder': 'Enter your username'}),
            'password1': PasswordInput(attrs={'placeholder': 'Enter a secure password'}),
            'password2': PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set admin privileges if the user selected 'is_admin'
        if self.cleaned_data['is_admin']:
            user.is_staff = True  # Grants admin privileges
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Form to authenticate an existing user with custom error messages.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label="Password"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override default error messages
        self.error_messages = {
            'invalid_login': "The username or password is incorrect. "
                              "Remember, both the username and password are case-sensitive.",
            'inactive': "Your account is inactive. Please contact support for assistance."
        }

    def clean(self):
        username = self.cleaned_data.get('username', '').lower()
        lockout_key = f"lockout_{username}"

        if cache.get(lockout_key):
            raise forms.ValidationError(
                "This account is temporarily locked due to too many failed login attempts. Try again in 5 minutes.",
                code="account_locked"
            )

        return super().clean()
