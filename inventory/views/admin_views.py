from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import F, Value, DateTimeField
from django.db.models.functions import Coalesce

from ..forms.admin_forms import EditUserForm
from ..utils.shared_utils import redirect_when_next, staff_required



@staff_required
@login_required(login_url='login')
def view_users(request):
    users = User.objects.annotate(
        last_seen=Coalesce('last_login', Value('1900-01-01', output_field=DateTimeField()))
    ).order_by('-last_seen')
    return render(request, 'inventory/admin/users.html', {'users': users})

@staff_required
@login_required(login_url='login')
def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.get_username().title()} was updated successfully.')
            return redirect('view-users')
    else:
        form = EditUserForm(instance=user)
    return render(request, 'inventory/admin/update-user.html', {'form': form, 'user': user})

@staff_required
@login_required(login_url='login')
def delete_user(request, user_id):
    """
    Deletes a customer and redirects to the customer list page.
    """
    user = get_object_or_404(User, id=user_id)
    user.delete()

    messages.success(request, f'User {user.get_username().title()} was deleted successfully.')
    return redirect_when_next(request, 'view-users')

