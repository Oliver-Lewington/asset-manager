from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from ..models import Asset
from .helpers import get_asset_counts, get_monthly_asset_data, get_recent_assets

# - Dashboard
@login_required(login_url='login/')
def dashboard(request):
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    # Get data using helper functions
    total_assets, active_assets, maintenance_assets, decommissioned_assets = get_asset_counts()
    months, active_assets_month, maintenance_assets_month, decommissioned_assets_month = get_monthly_asset_data(start_of_month)
    recent_assets = get_recent_assets()

    # Prepare context for the template
    context = {
        'total_assets': total_assets,
        'active_assets': active_assets,
        'maintenance_assets': maintenance_assets,
        'decommissioned_assets': decommissioned_assets,
        'months': months,
        'active_assets_month': active_assets_month,
        'maintenance_assets_month': maintenance_assets_month,
        'decommissioned_assets_month': decommissioned_assets_month,
        'recent_assets': recent_assets,
    }

    return render(request, 'inventory/dashboard.html', context)
