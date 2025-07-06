from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.cache import cache
from django.conf import settings

from ..utils.shared_utils import hash_username
from ..forms.authentication_forms import LoginForm, CreateUserForm

LOCKOUT_TIME = getattr(settings, 'LOCKOUT_TIME', 300)
MAX_ATTEMPTS = getattr(settings, 'MAX_ATTEMPTS', 5)
LOCKOUT_TIME_MINUTES = LOCKOUT_TIME // 60

# Helper Function
def authenticate_user(request, username, password):
    """Authenticate a user with the given username and password."""
    return authenticate(request, username=username, password=password)

def register(request):
    """
    Handle user registration.
    - Display a registration form.
    - Validate and save user data.
    - Log in the user after successful registration.
    """
    # If the user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        messages.warning(request, "You have already logged in, redirecting you to the dashboard.")
        return redirect('') 

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in after registration
            messages.success(request, f"Welcome, {user.username.title()}!")
            return redirect('')  # Redirect to dashboard after registration

    context = {'form': form}
    return render(request, 'inventory/authentication/register.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def login(request):
    def get_keys(username_input, ip_address):
        username_hash = hash_username(username_input)
        return (
            f"login_attempts_{username_hash}_{ip_address}",
            f"lockout_{username_hash}_{ip_address}"
        )

    form = LoginForm(request, data=request.POST or None)
    error_message = None

    if request.method == "POST":
        username_input = request.POST.get('username', '').strip().lower()
        ip_address = get_client_ip(request)
        attempt_key, lockout_key = get_keys(username_input, ip_address)
        lockout_error_message = f"Your account has been temporarily locked due to too many failed login attempts. "
            
        # Check lockout before validating form
        if cache.get(lockout_key):
            error_message = lockout_error_message
            form = LoginForm()  # Clear the form fields
        elif form.is_valid():
            # Successful login: clear attempts and lockout
            cache.delete(attempt_key)
            cache.delete(lockout_key)
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username.title()}!")
            return redirect("")
        else:
            # Failed login: increment attempts
            attempts = cache.get(attempt_key, 0) + 1
            cache.set(attempt_key, attempts, timeout=LOCKOUT_TIME)
            if attempts >= MAX_ATTEMPTS:
                cache.set(lockout_key, True, timeout=LOCKOUT_TIME)
                error_message = lockout_error_message
                form = LoginForm()  # Clear the form fields
            else:
                error_message =  f"The username or password you entered is incorrect. Attempt {attempts} of {MAX_ATTEMPTS} before your account will be locked for {LOCKOUT_TIME_MINUTES} minutes."

    if error_message:
        messages.error(request, error_message)

    return render(request, "inventory/authentication/login.html", {"form": form})
@login_required(login_url='login')
def delete_account(request):
    if request.method == "POST":
        # Delete the current user's account
        user = request.user
        user.delete()  # This will delete the user and all related data
        messages.success(request, "Your account has been successfully deleted, please register again if you would like to use the application.")
        return redirect('login')  # Redirect to the login page
    
    return render(request, 'inventory/authentication/delete-account.html')  # Confirmation page

@login_required(login_url='login')
def logout(request):
    """
    Handle user logout.
    - Log out the current user.
    - Redirect to the login page with a success message.
    """
    auth_logout(request)
    messages.success(request, "Logout successful!")
    return redirect('login')
