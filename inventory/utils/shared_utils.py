from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

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
    return user_passes_test(lambda u: u.is_active and u.is_staff)(view_func)
