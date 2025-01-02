from django.shortcuts import get_object_or_404
from ..models import Asset, MaintenanceHistory

def fetch_asset_by_id(asset_id):
    """
    Fetches an Asset object by its ID or raises a 404 error if not found.
    """
    return get_object_or_404(Asset, id=asset_id)

def fetch_maintenance_by_id(maintenance_id):
    """
    Fetches a MaintenanceHistory object by its ID or raises a 404 error if not found.
    """
    return get_object_or_404(MaintenanceHistory, id=maintenance_id)
