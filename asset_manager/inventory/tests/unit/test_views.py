from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.core.cache import cache

from inventory.models import Asset, MaintenanceHistory, Customer, User
from datetime import date

User = get_user_model()

class AssetViewsTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create a customer
        self.customer = Customer.objects.create(
            name='John Doe',
            email='johndoe@example.com',
            phone_number='+1234567890'
        )
        # Create an asset
        self.asset = Asset.objects.create(
            name='Asset 1',
            assigned_to=self.customer,
            warranty_expiry=date(2025, 12, 31),
            status=Asset.StatusChoices.ACTIVE,
            description='A test asset.'
        )
        # Log in with the user
        self.client.login(username='testuser', password='password')

    def test_view_assets(self):
        # Test the view for listing all assets
        url = reverse('view-assets')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/asset/assets.html')
        self.assertIn('page_obj', response.context)
        self.assertIn('assets_count', response.context)

    def test_search_assets(self):
        # Test asset search functionality
        url = reverse('view-assets') + '?search=Asset 1'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('search_query', response.context)
        self.assertEqual(response.context['search_query'], 'Asset 1')
        self.assertGreater(response.context['assets_count'], 0)

    def test_view_asset(self):
        # Test viewing a single asset
        url = reverse('view-asset', args=[self.asset.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/asset/view-asset.html')
        self.assertIn('asset', response.context)
        self.assertIn('maintenance_history', response.context)

    def test_create_asset(self):
        # Test creating a new asset
        url = reverse('create-asset')
        data = {
            'name': 'New Asset',
            'assigned_to': self.customer.id,
            'warranty_expiry': '2025-12-31',
            'status': Asset.StatusChoices.ACTIVE,
            'description': 'A new test asset.'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('view-assets'))
        self.assertEqual(Asset.objects.count(), 2)  # Asset should be created
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Your Asset has been created successfully.")

    def test_update_asset(self):
        # Test updating an existing asset
        url = reverse('update-asset', args=[self.asset.id])
        data = {
            'name': 'Updated Asset',
            'assigned_to': self.customer.id,
            'warranty_expiry': '2025-12-31',
            'status': Asset.StatusChoices.PENDING_MAINTENANCE,
            'description': 'Updated description.'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('view-asset', args=[self.asset.id]))
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.name, 'Updated Asset')
        self.assertEqual(self.asset.status, Asset.StatusChoices.PENDING_MAINTENANCE)

    def test_delete_asset(self):
        # Test deleting an asset
        url = reverse('delete-asset', args=[self.asset.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('view-assets'))
        self.assertEqual(Asset.objects.count(), 0)  # Asset should be deleted

    def test_pagination(self):
        # Test pagination for assets
        for i in range(10):  # Create 10 assets
            Asset.objects.create(
                name=f'Asset {i}', 
                assigned_to=self.customer,
                warranty_expiry=date(2025, 12, 31),
                status=Asset.StatusChoices.ACTIVE,
                description=f'Test asset {i}'
            )

        url = reverse('view-assets')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)
        self.assertTrue(response.context['page_obj'].has_next())  # Check if pagination exists
        self.assertEqual(len(response.context['page_obj']), 5)  # 5 assets per page

class CustomerViewsTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        # Create customers
        self.customer1 = Customer.objects.create(
            name='John Doe',
            email='johndoe@example.com',
            phone_number='+1234567890'
        )
        self.customer2 = Customer.objects.create(
            name='Jane Smith',
            email='janesmith@example.com',
            phone_number='+0987654321'
        )
        # Log in with the user
        self.client.login(username='testuser', password='password')

    def test_create_customer(self):
        # Test creating a new customer
        url = reverse('create-customer')
        data = {
            'name': 'New Customer',
            'email': 'newcustomer@example.com',
            'phone_number': '+1112223333'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('view-customers'))
        self.assertEqual(Customer.objects.count(), 3)  # One more customer should be created
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Customer has been created successfully.")

    def test_update_customer(self):
        # Test updating an existing customer
        url = reverse('update-customer', args=[self.customer1.id])
        data = {
            'name': 'Updated Customer',
            'email': 'updatedcustomer@example.com',
            'phone_number': '+2223334444'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('view-customer', args=[self.customer1.id]))
        self.customer1.refresh_from_db()
        self.assertEqual(self.customer1.name, 'Updated Customer')
        self.assertEqual(self.customer1.email, 'updatedcustomer@example.com')

    def test_delete_customer(self):
        # Test deleting an existing customer
        url = reverse('delete-customer', args=[self.customer2.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('view-customers'))
        self.assertEqual(Customer.objects.count(), 1)  # One customer should be deleted

class MaintenanceViewsTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create a customer
        self.customer = Customer.objects.create(
            name="John Doe", 
            email="johndoe@example.com", 
            phone_number="+1234567890"
        )

        # Create an asset for the customer
        self.asset = Asset.objects.create(
            name='Laptop',
            description='A new laptop for testing',
            status=Asset.StatusChoices.ACTIVE,
            assigned_to=self.customer
        )

        # Create a maintenance record for the asset
        self.maintenance = MaintenanceHistory.objects.create(
            asset=self.asset,
            performed_by=self.user,
            maintenance_type=MaintenanceHistory.MaintenanceType.REPAIR,
            description="Repaired broken screen"
        )

        # Log in with the user
        self.client.login(username='testuser', password='password')

    def test_create_maintenance(self):
        # Test creating a new maintenance record for an asset
        url = reverse('create-maintenance', args=[self.asset.id])
     
        data = {
            'asset': self.asset.id,
            'performed_by': self.user.id,
            'maintenance_type': MaintenanceHistory.MaintenanceType.CLEANING,
            'description': 'Cleaned the laptop thoroughly'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('view-asset', args=[self.asset.id]))
        self.assertEqual(MaintenanceHistory.objects.count(), 2)  # One more maintenance record should be created
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Maintenance record created successfully.")

    def test_update_maintenance(self):
        # Test updating an existing maintenance record
        url = reverse('update-maintenance', args=[self.maintenance.id])
        data = {
            'asset': self.asset.id,
            'performed_by': self.user.id,
            'maintenance_type': MaintenanceHistory.MaintenanceType.SOFTWARE_UPDATE,
            'description': 'Updated software to latest version'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('view-asset', args=[self.asset.id]))
        self.maintenance.refresh_from_db()
        self.assertEqual(self.maintenance.maintenance_type, MaintenanceHistory.MaintenanceType.SOFTWARE_UPDATE)
        self.assertEqual(self.maintenance.description, 'Updated software to latest version')

    def test_delete_maintenance(self):
        # Test deleting a maintenance record
        url = reverse('delete-maintenance', args=[self.maintenance.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('view-asset', args=[self.asset.id]))
        self.assertEqual(MaintenanceHistory.objects.count(), 0)  # One maintenance record should be deleted
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Maintenance record deleted successfully.")

class AuthenticationViewsTestCase(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_register_view_get(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/authentication/register.html')
        self.assertIn('form', response.context)

    def test_register_view_post_success(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Welcome, Newuser!", str(messages[0]))

    def test_register_view_already_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("You have already logged in", str(messages[0]))

    def test_login_view_get(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/authentication/login.html')
        self.assertIn('form', response.context)

    def test_login_view_post_invalid(self):
        cache.clear()  # Clear lockout/attempts before test
        url = reverse('login')
        data = {'username': self.username, 'password': 'wrongpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Invalid credentials", str(messages[0]))

    def test_login_view_post_invalid(self):
        cache.clear()  # Clear lockout/attempts before test
        url = reverse('login')
        data = {'username': self.username, 'password': 'wrongpass'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Invalid credentials", str(messages[0]))

    def test_login_view_lockout(self):
        url = reverse('login')
        data = {'username': self.username, 'password': 'wrongpass'}
        for _ in range(5):
            self.client.post(url, data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("locked for 5 minutes", str(messages[-1]))

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Logout successful!", str(messages[0]))

    def test_delete_account_view_get(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('delete-account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/authentication/delete-account.html')
        