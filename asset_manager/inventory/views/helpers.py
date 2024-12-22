from django.db.models import Count
from django.db.models.functions import TruncMonth
from ..models import Asset

def get_asset_counts():
    """Returns the count of total, active, maintenance, and decommissioned assets."""
    total_assets = Asset.objects.count()
    active_assets = Asset.objects.filter(status=Asset.StatusChoices.ACTIVE).count()
    maintenance_assets = Asset.objects.filter(status=Asset.StatusChoices.PENDING_MAINTENANCE).count()
    decommissioned_assets = Asset.objects.filter(status=Asset.StatusChoices.DECOMMISSIONED).count()

    return total_assets, active_assets, maintenance_assets, decommissioned_assets

def get_monthly_asset_data(start_of_month):
    """Returns monthly data for active, maintenance, and decommissioned assets."""
    monthly_data = (
        Asset.objects.filter(date_assigned__gte=start_of_month)
        .annotate(month=TruncMonth('date_assigned'))
        .values('month', 'status')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    active_assets_month = [0] * 12
    maintenance_assets_month = [0] * 12
    decommissioned_assets_month = [0] * 12

    for entry in monthly_data:
        month_index = entry['month'].month - 1
        if entry['status'] == 'Active':
            active_assets_month[month_index] = entry['count']
        elif entry['status'] == 'Pending Maintenance':
            maintenance_assets_month[month_index] = entry['count']
        elif entry['status'] == 'Decommissioned':
            decommissioned_assets_month[month_index] = entry['count']

    return months, active_assets_month, maintenance_assets_month, decommissioned_assets_month

def get_recent_assets(start_of_month):
    """Returns assets updated recently."""
    return Asset.objects.filter(date_assigned__gte=start_of_month).order_by('-date_assigned')#[:5]
