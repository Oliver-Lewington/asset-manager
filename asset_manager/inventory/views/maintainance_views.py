from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from datetime import date

from ..models import MaintenanceHistory
from ..forms import MaintenanceHistoryForm

# View to handle maintenance history record edit and deletion
@login_required(login_url='login')
def update_maintenance(request, maintenance_id):
    maintenance = get_object_or_404(MaintenanceHistory, id=maintenance_id)
    
    # Handle maintenance edit
    if request.method == 'POST':
        form = MaintenanceHistoryForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maintenance record updated successfully.')
            return redirect('asset_detail', asset_id=maintenance.asset.id)
    else:
        form = MaintenanceHistoryForm(instance=maintenance)

    return render(request, 'edit_maintenance.html', {'form': form})

# View to handle maintenance deletion
@login_required(login_url='login')
def delete_maintenance(request, maintenance_id):
    maintenance = get_object_or_404(MaintenanceHistory, id=maintenance_id)
    asset_id = maintenance.asset.id
    maintenance.delete()

    messages.success(request, 'Maintenance record deleted successfully.')

    return redirect('asset_detail', asset_id=asset_id)