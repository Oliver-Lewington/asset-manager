from ..models import Customer

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

# --- Customer-related Functions ---
def get_customer_by_id(customer_id):
    """
    Fetches a Customer object by its ID or returns a 404 error if not found.
    """
    return get_object_or_404(Customer, id=customer_id)

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

def get_customer_asset_counts():
    """
    Returns the count of distinct customers with assets assigned.
    """
    return Customer.objects.filter(asset__isnull=False).distinct().count()
