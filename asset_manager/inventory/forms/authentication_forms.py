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

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set admin privileges if the user selected 'can_delete'
        if self.cleaned_data['can_delete']:
            user.is_staff = True  # Grants admin privileges
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Form to authenticate an existing user.
    """
    username = forms.CharField(
        widget=TextInput(attrs={'placeholder': 'Enter your username'}),
        label="Username"
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={'placeholder': 'Enter your password'}),
        label="Password"
    )
