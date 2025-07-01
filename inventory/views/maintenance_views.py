from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..forms.maintenance_forms import MaintenanceHistoryForm

from ..utils.asset_utils import get_asset_by_id
from ..utils.shared_utils import redirect_when_next, staff_required
from ..utils.maintenance_utils import get_maintenance_by_id

@login_required(login_url='login')
def create_maintenance(request, asset_id):
    """
    Displays a form to create a new maintenance record for a specific asset.
    On form submission, saves the maintenance record.
    """
    asset = get_asset_by_id(asset_id)  # Utility function to fetch asset or return 404

    if request.method == 'POST':
        form = MaintenanceHistoryForm(request.POST, initial={'asset': asset}, user=request.user)
        if not request.user.is_staff:  # Check if the user is not staff
            form.fields['performed_by'].initial = request.user  # Set 'performed_by' to current user if not staff
        if form.is_valid():
            maintenance_record = form.save(commit=False)
            maintenance_record.asset = asset  # Ensure the asset is correctly set

            maintenance_record.save()
            messages.success(request, 'Maintenance record created successfully.')
            return redirect_when_next(request, 'view-asset', asset_id=asset.id)
    else:
        form = MaintenanceHistoryForm(initial={'asset': asset}, user=request.user)

    return render(request, 'inventory/maintenance/create-maintenance.html', {
        'form': form,
        'asset': asset,
    })



@login_required(login_url='login')
def update_maintenance(request, maintenance_id):
    """
    Displays a form to update an existing maintenance record.
    On form submission, saves the changes.
    """
    maintenance = get_maintenance_by_id(maintenance_id)  # Utility function to fetch maintenance or return 404

    if request.method == 'POST':
        form = MaintenanceHistoryForm(request.POST, instance=maintenance, user=request.user)
        if not request.user.is_staff:  # Check if the user is not staff
            form.fields['performed_by'].initial = maintenance.performed_by  # Set 'performed_by' to current user if not staff
        if form.is_valid():
            form.save()
            messages.success(request, 'Maintenance record updated successfully.')
            return redirect_when_next(request, 'view-asset', asset_id=maintenance.asset.id)
    else:
        form = MaintenanceHistoryForm(instance=maintenance, user=request.user)
        if not request.user.is_staff:  # Set 'performed_by' to current user if not staff
            form.fields['performed_by'].initial = request.user

    return render(request, 'inventory/maintenance/update-maintenance.html', {
        'form': form,
        'maintenance': maintenance,
    })



@staff_required
@login_required(login_url='login')
def delete_maintenance(request, maintenance_id):
    """
    Deletes a maintenance record and redirects to the asset's detail view.
    """
    maintenance = get_maintenance_by_id(maintenance_id)  # Utility function to fetch maintenance or return 404
    asset_id = maintenance.asset.id  # Store asset ID before deleting the maintenance record
    maintenance.delete()
    messages.success(request, 'Maintenance record deleted successfully.')
    return redirect_when_next(request, 'view-asset', asset_id=asset_id)
