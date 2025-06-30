from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.cache import cache

from ..utils.shared_utils import hash_username
from ..forms.authentication_forms import LoginForm, CreateUserForm

MAX_ATTEMPTS = 5
LOCKOUT_TIME = 5 * 60  # 5 minutes in seconds

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

def login(request):
    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":
        username = hash_username(request.POST.get("username", "").strip().lower())
        lockout_key = f"lockout_{username}"
        attempt_key = f"login_attempts_{username}"
        
        # If form is invalid (invalid credentials)
        attempts = cache.get(attempt_key, 0) + 1
        cache.set(attempt_key, attempts, timeout=LOCKOUT_TIME)

        # Check if the user is currently locked out
        if cache.get(lockout_key):
            return render(request, "inventory/authentication/login.html", {"form": form})

        if attempts >= MAX_ATTEMPTS:         
            cache.set(lockout_key, True, timeout=LOCKOUT_TIME)
            return render(request, "inventory/authentication/login.html", {"form": form})

        if form.is_valid():
            user = form.get_user()
            cache.delete(attempt_key)
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username.title()}!")
            return redirect("") 

    return render(request, "inventory/authentication/login.html", {"form": form})

@login_required(login_url='login')
def delete_account(request):
    if request.method == "POST":
        # Delete the current user's account
        user = request.user
        user.delete()
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
