from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from ..forms.authentication_forms import LoginForm, CreateUserForm

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
    # If the user is already logged in, redirect to dashboard or home
    if request.user.is_authenticated:
        messages.warning(request, "You have already logged in, redirecting you to the dashboard.")
        return redirect('')  # Change 'dashboard' to the URL you want

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
    """
    Handle user login.
    - Display a login form.
    - Authenticate and log in the user if credentials are valid.
    - Redirect to the dashboard upon successful login.
    """
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate_user(request, username, password)  # Use helper function

            if user is not None:
                auth_login(request, user)  # Log the user in
                messages.success(request, f"Welcome back, {username.title()}!")
                return redirect('')  # Redirect to the dashboard (or any page you want)
            else:
                messages.error(request, "Invalid username or password.")

    context = {'form': form}
    return render(request, 'inventory/authentication/login.html', context)

@login_required(login_url='login')
def delete_account(request):
    if request.method == "POST":
        # Delete the current user's account
        user = request.user
        user.delete()
        messages.success(request, "Your account has been successfully deleted, please register again if you would like to use the application.")
        return redirect('login')  # Redirect to the login page or homepage
    
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
