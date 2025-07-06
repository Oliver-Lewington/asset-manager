from django import forms
from django.conf import settings
from django.core.cache import cache
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from ..utils.shared_utils import hash_username

LOCKOUT_TIME = getattr(settings, 'LOCKOUT_TIME', 300)  # default 5 minutes in seconds
MAX_ATTEMPTS = getattr(settings, 'MAX_ATTEMPTS', 5)
LOCKOUT_TIME_MINUTES = LOCKOUT_TIME // 60


class CreateUserForm(UserCreationForm):
    """
    Form to create a new user with optional admin privileges.
    """

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
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
        self.error_messages = {
            'invalid_login': (
                "The username or password you entered is incorrect. "
                "Please check your credentials and try again."
            ),
            'inactive': (
                "Your account is currently inactive. "
                "Please contact support if you believe this is an error."
            ),
        }
