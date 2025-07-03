from django.shortcuts import redirect
from django.contrib import messages

from functools import wraps
import hashlib

# --- Redirection Helper Functions ---
def redirect_when_next(request, default_url='/', **kwargs):
    """
    Redirects to the 'next' URL parameter if available, otherwise redirects to the default URL.
    Accepts dynamic URL parameters for flexibility (e.g., asset_id or customer_id).
    """
    next_url = request.GET.get('next', default_url)  # Default to given URL if 'next' not provided
    return redirect(next_url, **kwargs) if kwargs else redirect(next_url)

def hash_username(username):
    return hashlib.sha256(username.encode('utf-8')).hexdigest()

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}, Staff: {request.user.is_staff}")
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page. Please log in below.")
            return redirect('login')
        if not request.user.is_staff:
            from django.contrib.auth import logout
            logout(request)
            messages.error(
                request,
                "Access denied: You do not have sufficient permissions to access this page. "
                "If you believe this is an error, please contact a system administrator."
            )
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view