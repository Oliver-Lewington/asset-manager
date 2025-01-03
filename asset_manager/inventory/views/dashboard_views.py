from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..utils import get_asset_counts, get_current_month_maintenance_data, get_recent_assets

# - Dashboard
@login_required(login_url='login/')
def dashboard(request):
    # Get data using helper functions
    recent_assets = get_recent_assets(7)
    total_assets, active_assets, maintenance_assets, decommissioned_assets = get_asset_counts()
    
    # Get current month maintenance data
    repair_count, software_update_count, cleaning_count, other_count = get_current_month_maintenance_data()

    # Prepare context for the template
    context = {
        'total_assets': total_assets,
        'active_assets': active_assets,
        'maintenance_assets': maintenance_assets,
        'decommissioned_assets': decommissioned_assets,
        'recent_assets': recent_assets,
        'repair_count': repair_count,
        'software_update_count': software_update_count,
        'cleaning_count': cleaning_count,
        'other_count': other_count,
    }

    return render(request, 'inventory/dashboard.html', context)


