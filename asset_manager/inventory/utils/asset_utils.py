from datetime import timedelta, date, datetime

from django.shortcuts import get_object_or_404

from ..models import Asset

# --- Asset-related Functions ---
def get_asset_by_id(asset_id):
    """
    Fetches an Asset by its ID or returns a 404 error if not found.
    """
    return get_object_or_404(Asset, id=asset_id)


def get_filtered_assets(search_query=None):
    """
    Fetches all assets or filters them based on the search query.
    If no search query is provided, returns all assets.
    """
    return Asset.objects.filter(name__icontains=search_query) if search_query else Asset.objects.all()


def get_asset_metrics(assets):
    """
    Calculates various asset metrics: Active, Pending Maintenance, Decommissioned,
    Under Warranty, and Out of Warranty assets.
    Returns a dictionary with each metric.
    """
    metrics = {
        'active_assets': assets.filter(status=Asset.StatusChoices.ACTIVE).count(),
        'maintenance_assets': assets.filter(status=Asset.StatusChoices.PENDING_MAINTENANCE).count(),
        'decommissioned_assets': assets.filter(status=Asset.StatusChoices.DECOMMISSIONED).count(),
        'assets_under_warranty': assets.filter(warranty_expiry__gte=date.today()).count(),
        'assets_out_of_warranty': assets.filter(warranty_expiry__lt=date.today()).count(),
        'assets_not_applicable': assets.filter(warranty_expiry__isnull=True).count(),
    }
    return metrics

def get_asset_assignments():
    # Assigned and unassigned assets metrics
    assigned_assets = Asset.objects.filter(assigned_to__isnull=False).count()
    unassigned_assets = Asset.objects.filter(assigned_to__isnull=True).count()

    return {
        'assigned_assets': assigned_assets,
        'unassigned_assets': unassigned_assets,
    }

def get_asset_counts():
    """
    Returns the count of total, active, maintenance, and decommissioned assets.
    """
    return (
        Asset.objects.count(),
        Asset.objects.filter(status=Asset.StatusChoices.ACTIVE).count(),
        Asset.objects.filter(status=Asset.StatusChoices.PENDING_MAINTENANCE).count(),
        Asset.objects.filter(status=Asset.StatusChoices.DECOMMISSIONED).count()
    )

def get_recent_assets(number_of_days):
    """
    Returns a list of assets assigned within the past month, ordered by the most recent first.
    """
    one_month_ago = datetime.today() - timedelta(days=number_of_days)  # Set the range to the last month
    return Asset.objects.filter(date_assigned__gte=one_month_ago).order_by('-last_updated')


def get_asset_types():
    """
    Returns a list of distinct asset types currently in the system.
    """
    return Asset.objects.values('asset_type').distinct()

