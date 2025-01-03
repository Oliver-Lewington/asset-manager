from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    """
    Form to create a new user with optional admin privileges.
    """
    can_delete = forms.BooleanField(
        required=False,
        initial=False,
        label="Can delete records",
        help_text="Grant admin privileges to delete items.",
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'can_delete']
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
        # Override default error messages
        self.error_messages = {
            'invalid_login': "The username or password is incorrect. "
                              "Remember, both the username and password are case-sensitive.",
            'inactive': "Your account is inactive. Please contact support for assistance."
        }


