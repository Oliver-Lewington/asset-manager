from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from datetime import date

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(
        max_length=20,  # Accommodates phone numbers with spaces
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?[\d\s]+$',
                message="Phone number must start with an optional '+' followed by digits, with optional spaces."
            )
        ]
    )
    email = models.CharField(max_length=200, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        PENDING_MAINTENANCE = 'Pending Maintenance', 'Pending Maintenance'
        DECOMMISSIONED = 'Decommissioned', 'Decommissioned'

    name = models.CharField(max_length=200, null=True)
    assigned_to = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="assignment")
    warranty_expiry = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        null=False
    )
    description = models.CharField(max_length=450, null=True, blank=True)
    date_assigned = models.DateTimeField(auto_now_add=True)

    @property
    def is_warranty_pending(self):
        """
        Returns True if the warranty expiry date is in the future; False otherwise.
        """
        if self.warranty_expiry:
            return self.warranty_expiry >= date.today()
        return False

    def __str__(self):
        return self.name

class MaintenanceHistory(models.Model):
    """
    Tracks maintenance activities performed on assets.
    """
    class MaintenanceType(models.TextChoices):
        REPAIR = 'Repair', 'Repair'
        SOFTWARE_UPDATE = 'Software Update', 'Software Update'
        CLEANING = 'Cleaning', 'Cleaning'
        OTHER = 'Other', 'Other'

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="maintenances")
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="maintenances")
    maintenance_type = models.CharField(max_length=50, choices=MaintenanceType.choices, null=False)
    description = models.TextField(null=True, blank=True)  # Optional notes about the maintenance
    date_maintained = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Maintenance: {self.asset.name} ({self.maintenance_type})"