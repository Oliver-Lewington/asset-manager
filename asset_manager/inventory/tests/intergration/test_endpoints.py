from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from inventory.models import Asset, Customer, MaintenanceHistory


class EndpointIntegrationTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpass"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.customer = Customer.objects.create(name="John Doe", email="john@example.com")
        self.asset = Asset.objects.create(
            name="Asset1", status="Active", assigned_to=self.customer
        )
        self.maintenance = MaintenanceHistory.objects.create(
            asset=self.asset,
            performed_by=self.user,
            maintenance_type=MaintenanceHistory.MaintenanceType.REPAIR if hasattr(MaintenanceHistory, "MaintenanceType") else "Repair",
            description="Initial repair"
        )

    def test_login_logout(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("login"), {"username": self.username, "password": self.password})
        self.assertIn(response.status_code, (302, 200))
        response = self.client.get(reverse("logout"))
        self.assertIn(response.status_code, (302, 200))

    def test_register(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        })
        self.assertIn(response.status_code, (302, 200))

    def test_assets_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("view-assets"))
        self.assertEqual(response.status_code, 200)

    def test_assets_create(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("create-asset"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("create-asset"), {
            "name": "Test Asset",
            "status": "Active",
        })
        self.assertIn(response.status_code, (302, 200))

    def test_assets_update(self):
        self.client.login(username=self.username, password=self.password)
        asset = Asset.objects.create(name="Old Asset", status="Active")
        response = self.client.get(reverse("update-asset", args=[asset.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("update-asset", args=[asset.id]), {
            "name": "Updated Asset",
            "status": "Inactive",
        })
        self.assertIn(response.status_code, (302, 200))

    def test_assets_delete(self):
        self.client.login(username=self.username, password=self.password)
        asset = Asset.objects.create(name="Delete Asset", status="Active")
        response = self.client.post(reverse("delete-asset", args=[asset.id]))
        self.assertIn(response.status_code, (302, 200))

    def test_customers_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("view-customers"))
        self.assertEqual(response.status_code, 200)

    def test_customers_create(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("create-customer"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("create-customer"), {
            "name": "Test Customer",
            "email": "customer@example.com",
        })
        self.assertIn(response.status_code, (302, 200))

    def test_customers_update(self):
        self.client.login(username=self.username, password=self.password)
        customer = Customer.objects.create(name="Old Customer", email="old@example.com")
        response = self.client.get(reverse("update-customer", args=[customer.id]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("update-customer", args=[customer.id]), {
            "name": "Updated Customer",
            "email": "updated@example.com",
        })
        self.assertIn(response.status_code, (302, 200))

    def test_customers_delete(self):
        self.client.login(username=self.username, password=self.password)
        customer = Customer.objects.create(name="Delete Customer", email="del@example.com")
        response = self.client.post(reverse("delete-customer", args=[customer.id]))
        self.assertIn(response.status_code, (302, 200))

    def test_asset_detail_view(self):
            self.client.login(username=self.username, password=self.password)
            response = self.client.get(reverse("view-asset", args=[self.asset.id]))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, self.asset.name)

    def test_customer_detail_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("view-customer", args=[self.customer.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer.name)

    def test_asset_search(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("view-assets") + "?search=Asset1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Asset1")

    def test_assets_pagination(self):
        self.client.login(username=self.username, password=self.password)
        for i in range(10):
            Asset.objects.create(
                name=f"Asset {i}", status="Active", assigned_to=self.customer
            )
        url = reverse("view-assets")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("page_obj", response.context)
        self.assertTrue(response.context["page_obj"].has_next())

    def test_customer_search(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("view-customers") + "?search=John"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")

    def test_create_maintenance(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("create-maintenance", args=[self.asset.id])
        data = {
            "asset": self.asset.id,
            "performed_by": self.user.id,
            "maintenance_type": self.maintenance.maintenance_type,
            "description": "Routine check"
        }
        response = self.client.post(url, data)
        self.assertIn(response.status_code, (302, 200))

    def test_update_maintenance(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("update-maintenance", args=[self.maintenance.id])
        data = {
            "asset": self.asset.id,
            "performed_by": self.user.id,
            "maintenance_type": self.maintenance.maintenance_type,
            "description": "Updated description"
        }
        response = self.client.post(url, data)
        self.assertIn(response.status_code, (302, 200))

    def test_delete_maintenance(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("delete-maintenance", args=[self.maintenance.id])
        response = self.client.post(url)
        self.assertIn(response.status_code, (302, 200))

    def test_delete_account(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse("delete-account")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertIn(response.status_code, (302, 200))