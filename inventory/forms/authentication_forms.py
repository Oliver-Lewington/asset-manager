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
        if self.cleaned_data['is_admin']:
            user.is_staff = True
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Form to authenticate an existing user with custom error messages and lockout logic.
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
                f"The username or password you entered is incorrect. "
                f"Please check your credentials and try again. "
                f"Attempt {{attempts}} of {MAX_ATTEMPTS}."
            ),
            'inactive': (
                "Your account is currently inactive. "
                "Please contact support if you believe this is an error."
            ),
            'locked': (
                f"Your account has been temporarily locked due to too many failed login attempts. "
                f"Please wait {LOCKOUT_TIME_MINUTES} minutes before trying again. "
                "If you need immediate access, contact support."
            ),
        }

    def clean(self):
        username_input = self.cleaned_data.get('username', '').lower()
        username_hash = hash_username(username_input)
        lockout_key = f"lockout_{username_hash}"
        attempt_key = f"login_attempts_{username_hash}"

        # Check if the user is currently locked out
        if cache.get(lockout_key):
            raise forms.ValidationError(
                {'__all__': [self.error_messages['locked']]},
                code="locked"
            )

        try:
            return super().clean()
        except forms.ValidationError as e:
            # Increment login attempts on failure
            attempts = cache.get(attempt_key, 0) + 1
            cache.set(attempt_key, attempts, timeout=LOCKOUT_TIME)

            # Lock the account if max attempts reached
            if attempts >= MAX_ATTEMPTS:
                cache.set(lockout_key, True, timeout=LOCKOUT_TIME)

            # Customize error message for invalid login
            if e.code == 'invalid_login':
                raise forms.ValidationError(
                    {'__all__': [
                        self.error_messages['invalid_login'].format(attempts=attempts),
                        "Note: Both fields are case-sensitive.",
                        (
                            f"After {MAX_ATTEMPTS} failed attempts, your account will be temporarily "
                            f"locked for {LOCKOUT_TIME_MINUTES} minutes."
                        )
                    ]},
                    code="invalid_login"
                )
            raise
