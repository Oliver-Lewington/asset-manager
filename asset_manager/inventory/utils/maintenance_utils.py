from django.utils import timezone
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from ..models import Customer, MaintenanceHistory

# --- MaintenanceHistory-related Functions ---
def get_maintenance_by_id(maintenance_id):
    """
    Fetches a MaintenanceHistory object by its ID or returns a 404 error if not found.
    """
    return get_object_or_404(MaintenanceHistory, id=maintenance_id)

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
