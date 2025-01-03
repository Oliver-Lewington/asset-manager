from datetime import timedelta, date
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import Http404
from ..models import Asset, Customer, MaintenanceHistory

# -- Asset Utils TestsCase --
from ..utils.asset_utils import (
    get_asset_by_id, get_filtered_assets, get_asset_metrics, get_asset_assignments,
    get_asset_counts, get_recent_assets
)

class AssetUtilsTestCase(TestCase):
    def setUp(self):
        # Create customers
        self.customer1 = Customer.objects.create(name="John Doe", email="john.doe@example.com")

        # Create assets
        self.asset1 = Asset.objects.create(name="Laptop A", assigned_to=self.customer1, 
                                           warranty_expiry=date.today() + timedelta(days=100),
                                           status=Asset.StatusChoices.ACTIVE)
        self.asset2 = Asset.objects.create(name="Printer B", warranty_expiry=date.today() - timedelta(days=50),
                                           status=Asset.StatusChoices.PENDING_MAINTENANCE)
        self.asset3 = Asset.objects.create(name="Desktop C", assigned_to=None, 
                                           status=Asset.StatusChoices.DECOMMISSIONED)
        self.asset4 = Asset.objects.create(name="Monitor D", warranty_expiry=None, 
                                           status=Asset.StatusChoices.ACTIVE)

    def test_get_asset_by_id(self):
        asset = get_asset_by_id(self.asset1.id)
        self.assertEqual(asset, self.asset1)

    def test_get_filtered_assets(self):
        assets = get_filtered_assets("Laptop")
        self.assertIn(self.asset1, assets)
        self.assertNotIn(self.asset2, assets)

    def test_get_asset_metrics(self):
        assets = Asset.objects.all()
        metrics = get_asset_metrics(assets)
        self.assertEqual(metrics['active_assets'], 2)
        self.assertEqual(metrics['maintenance_assets'], 1)
        self.assertEqual(metrics['decommissioned_assets'], 1)
        self.assertEqual(metrics['assets_under_warranty'], 1)
        self.assertEqual(metrics['assets_out_of_warranty'], 1)
        self.assertEqual(metrics['assets_not_applicable'], 2)

    def test_get_asset_assignments(self):
        assignments = get_asset_assignments()
        self.assertEqual(assignments['assigned_assets'], 1)
        self.assertEqual(assignments['unassigned_assets'], 3)

    def test_get_asset_counts(self):
        total, active, maintenance, decommissioned = get_asset_counts()
        self.assertEqual(total, 4)
        self.assertEqual(active, 2)
        self.assertEqual(maintenance, 1)
        self.assertEqual(decommissioned, 1)

    def test_get_recent_assets(self):
        recent_assets = get_recent_assets(30)
        self.assertIn(self.asset1, recent_assets)
        self.assertIn(self.asset2, recent_assets)
        self.assertIn(self.asset3, recent_assets)
        self.assertIn(self.asset4, recent_assets)

# -- Customer Utils TestsCase --
from ..utils.customer_utils import (
    get_customer_by_id, get_filtered_customers, get_customer_metrics
)

class CustomerUtilsTestCase(TestCase):
    def setUp(self):
        # Create customers
        self.customer1 = Customer.objects.create(name="John Doe", email="john.doe@example.com")
        self.customer2 = Customer.objects.create(name="Jane Smith", email="jane.smith@example.com")
        self.customer3 = Customer.objects.create(name="Bob Brown", email="bob.brown@example.com")

        # Create assets assigned to customers
        Asset.objects.create(name="Laptop A", assigned_to=self.customer1)
        Asset.objects.create(name="Printer B", assigned_to=self.customer1)
        Asset.objects.create(name="Desktop C", assigned_to=self.customer2)

    def test_get_customer_by_id(self):
        customer = get_customer_by_id(self.customer1.id)
        self.assertEqual(customer, self.customer1)

    def test_get_filtered_customers(self):
        filtered_customers = get_filtered_customers("John")
        self.assertIn(self.customer1, filtered_customers)
        self.assertNotIn(self.customer2, filtered_customers)

    def test_get_customer_metrics(self):
        customers = Customer.objects.all()
        metrics = get_customer_metrics(customers)

        self.assertEqual(metrics['total_customers'], 3)
        self.assertEqual(metrics['customers_with_assets'], 2)
        self.assertEqual(metrics['customers_without_assets'], 1)

# -- Maintainance Utils TestsCase --
from ..utils.maintenance_utils import (
    get_maintenance_by_id, get_current_month_maintenance_data
    )

# -- Maintenance Utils TestCase --

from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from ..models import Customer, Asset, MaintenanceHistory
from ..utils.maintenance_utils import get_maintenance_by_id, get_current_month_maintenance_data

class MaintenanceUtilsTestCase(TestCase):
    def setUp(self):
        # Create a user for performed_by field in MaintenanceHistory
        self.user = User.objects.create_user(username="tech", password="password123")

        # Create customers
        self.customer1 = Customer.objects.create(name="John Doe", email="john.doe@example.com")
        self.customer2 = Customer.objects.create(name="Jane Smith", email="jane.smith@example.com")

        # Create assets
        self.asset1 = Asset.objects.create(name="Laptop A", assigned_to=self.customer1, status=Asset.StatusChoices.ACTIVE)
        self.asset2 = Asset.objects.create(name="Printer B", assigned_to=self.customer2, status=Asset.StatusChoices.ACTIVE)

        # Create maintenance history entries with timezone-aware datetimes
        self.maintenance1 = MaintenanceHistory.objects.create(
            id = 1,
            asset=self.asset1,
            performed_by=self.user,
            maintenance_type="Repair",
            description="Repaired motherboard",
            date_maintained=timezone.now() - timedelta(days=10)
        )
        self.maintenance2 = MaintenanceHistory.objects.create(
            id = 2,
            asset=self.asset2,
            performed_by=self.user,
            maintenance_type="Software Update",
            description="Updated drivers",
            date_maintained=timezone.now() - timedelta(days=5)
        )

    def test_get_maintenance_by_id(self):
        # Test retrieving maintenance history by ID
        maintenance = get_maintenance_by_id(self.maintenance1.id)
        self.assertEqual(maintenance, self.maintenance1)

        # Test retrieving non-existent maintenance history (expecting Http404)
        with self.assertRaises(Http404):
            get_maintenance_by_id(9999)

    def test_get_current_month_maintenance_data(self):
        # Test counting maintenance activities in the current month
        repair_count, software_update_count, cleaning_count, other_count = get_current_month_maintenance_data()
        self.assertEqual(repair_count, 1)
        self.assertEqual(software_update_count, 1)
        self.assertEqual(cleaning_count, 0)
        self.assertEqual(other_count, 0)

        # Test when no maintenance is performed in the current month
        # (change the date_maintained of maintenance2 to next month for testing)
        self.maintenance2.date_maintained = timezone.now() + timedelta(days=40)  # 40 days later, which is next month
        self.maintenance2.save()

        repair_count, software_update_count, cleaning_count, other_count = get_current_month_maintenance_data()
        self.assertEqual(repair_count, 1)
        self.assertEqual(software_update_count, 1)
        self.assertEqual(cleaning_count, 0)
        self.assertEqual(other_count, 0)

        # Test when no maintenance is performed in the current month
        # (change the date_maintained of maintenance2 to next month for testing)
        self.maintenance2.date_maintained = timezone.now() + timedelta(days=10)
        self.maintenance2.save()

        repair_count, software_update_count, cleaning_count, other_count = get_current_month_maintenance_data()
        self.assertEqual(repair_count, 1)
        self.assertEqual(software_update_count, 1)
        self.assertEqual(cleaning_count, 0)
        self.assertEqual(other_count, 0)