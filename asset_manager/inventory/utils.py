from datetime import timedelta, date, datetime

from django.utils import timezone
from django.db.models import Count, Q
from django.shortcuts import redirect, get_object_or_404

from .models import Asset, Customer, MaintenanceHistory

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


def get_current_month_maintenance_data():
    """
    Returns the count of different types of maintenance activities performed in the current month.
    """
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    maintenance_data = (
        MaintenanceHistory.objects.filter(date_maintained__gte=start_of_month)
        .values('maintenance_type')
        .annotate(count=Count('id'))
    )

    # Initialize counts for each maintenance type
    repair_count = 0
    software_update_count = 0
    cleaning_count = 0
    other_count = 0

    # Loop through data and map counts to maintenance types
    for entry in maintenance_data:
        if entry['maintenance_type'] == 'Repair':
            repair_count = entry['count']
        elif entry['maintenance_type'] == 'Software Update':
            software_update_count = entry['count']
        elif entry['maintenance_type'] == 'Cleaning':
            cleaning_count = entry['count']
        elif entry['maintenance_type'] == 'Other':
            other_count = entry['count']

    return repair_count, software_update_count, cleaning_count, other_count


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


# --- Customer-related Functions ---
def get_customer_by_id(customer_id):
    """
    Fetches a Customer object by its ID or returns a 404 error if not found.
    """
    return get_object_or_404(Customer, id=customer_id)


def get_user_asset_counts():
    """
    Returns the count of distinct customers with assets assigned.
    """
    return Customer.objects.filter(asset__isnull=False).distinct().count()


# --- MaintenanceHistory-related Functions ---
def get_maintenance_by_id(maintenance_id):
    """
    Fetches a MaintenanceHistory object by its ID or returns a 404 error if not found.
    """
    return get_object_or_404(MaintenanceHistory, id=maintenance_id)

# --- Customer-related Functions ---
def get_filtered_customers(search_query):
    """Filters customers based on search query."""
    if search_query:
        return Customer.objects.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    return Customer.objects.all()

def get_customer_metrics(customers):
    """Calculates quick info metrics for customers."""
    total_customers = customers.count()
    customers_with_assets = customers.annotate(asset_count=Count('assignment')).filter(asset_count__gt=0).count()
    customers_without_assets = total_customers - customers_with_assets

    return {
        'total_customers': total_customers,
        'customers_with_assets': customers_with_assets,
        'customers_without_assets': customers_without_assets,
    }

# --- Redirection Helper Functions ---
def redirect_when_next(request, default_url='/', **kwargs):
    """
    Redirects to the 'next' URL parameter if available, otherwise redirects to the default URL.
    Accepts dynamic URL parameters for flexibility (e.g., asset_id or customer_id).
    """
    next_url = request.GET.get('next', default_url)  # Default to given URL if 'next' not provided
    return redirect(next_url, **kwargs) if kwargs else redirect(next_url)
