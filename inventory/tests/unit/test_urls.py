from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from inventory.models import Customer, Asset, MaintenanceHistory

class TestUrls(TestCase):
    def setUp(self):
        # Create a user for authentication-related tests
        self.user = get_user_model().objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')  # Log the user in for access control testing

        # Create assets and customers for tests that require them
        self.customer = Customer.objects.create(name="John Doe", email="john.doe@example.com")
        self.asset = Asset.objects.create(name="Laptop A", assigned_to=self.customer)
        self.maintenance = MaintenanceHistory.objects.create(
            asset=self.asset,
            maintenance_type="Repair",
            description="Repaired motherboard",
            date_maintained=timezone.now()
        )


    def test_dashboard_url(self):
        url = reverse('')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # Asset URLs
    def test_view_assets_url(self):
        url = reverse('view-assets')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_asset_url(self):
        url = reverse('view-asset', kwargs={'asset_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) # Will fail ass asset retrieval will return a 200 response

    def test_create_asset_url(self):
        url = reverse('create-asset')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_asset_url(self):
        url = reverse('update-asset', kwargs={'asset_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_asset_url(self):
        url = reverse('delete-asset', kwargs={'asset_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # Maintenance URLs
    def test_create_maintenance_url(self):
        url = reverse('create-maintenance', kwargs={'asset_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_maintenance_url(self):
        url = reverse('update-maintenance', kwargs={'maintenance_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_maintenance_url(self):
        url = reverse('delete-maintenance', kwargs={'maintenance_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # Customer URLs
    def test_view_customers_url(self):
        url = reverse('view-customers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_customer_url(self):
        url = reverse('create-customer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_customer_url(self):
        url = reverse('view-customer', kwargs={'customer_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_customer_url(self):
        url = reverse('update-customer', kwargs={'customer_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_customer_url(self):
        url = reverse('delete-customer', kwargs={'customer_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    # Authentication URLs
    def test_login_url(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_register_url(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_delete_account_url(self):
        url = reverse('delete-account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
