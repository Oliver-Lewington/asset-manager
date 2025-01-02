from django.shortcuts import redirect

from ..models import Asset
from datetime import date

def get_filtered_assets(search_query):
    """
    Fetch assets filtered by the search query.
    If no query is provided, return all assets.
    """
    return Asset.objects.filter(name__icontains=search_query) if search_query else Asset.objects.all()

def get_asset_metrics(assets):
    """
    Calculate various asset metrics: Active, Pending Maintenance, Decommissioned, 
    Under Warranty, and Out of Warranty assets.
    """
    active_assets = assets.filter(status=Asset.StatusChoices.ACTIVE).count()
    maintenance_assets = assets.filter(status=Asset.StatusChoices.PENDING_MAINTENANCE).count()
    decommissioned_assets = assets.filter(status=Asset.StatusChoices.DECOMMISSIONED).count()
    assets_under_warranty = assets.filter(warranty_expiry__gte=date.today()).count()
    assets_out_of_warranty = assets.filter(warranty_expiry__lt=date.today()).count()

    return {
        'active_assets': active_assets,
        'maintenance_assets': maintenance_assets,
        'decommissioned_assets': decommissioned_assets,
        'assets_under_warranty': assets_under_warranty,
        'assets_out_of_warranty': assets_out_of_warranty
    }

from django.shortcuts import redirect

def redirect_when_next(request, default_url='/', **kwargs):
    """
    Handles redirection based on the 'next' parameter, and allows dynamic URL parameters like asset_id or customer_id.
    """
    next_url = request.GET.get('next', default_url)  # Default to the given default_url if 'next' is not provided
    
    # Dynamically build the URL with the passed keyword arguments (e.g., asset_id or customer_id)
    if kwargs:
        return redirect(next_url, **kwargs)
    return redirect(next_url)
