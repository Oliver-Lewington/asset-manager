from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator, MinLengthValidator

class Customer(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-zA-Z])(?=.*[a-zA-Z0-9]).+$',
                message="Name must contain at least one letter and cannot consist solely of special characters or numbers."
            )
        ]
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,  # Allows empty input in forms
        validators=[
            RegexValidator(
                regex=r'^\+?(\(\d{1,4}\)|\d{1,4})?[\s\-]?\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{1,4}$',
                message="Phone number must start with an optional '+' followed by digits, with optional spaces, parentheses, or hyphens."
            )
        ]
    )
    email = models.CharField(
        max_length=200,
        unique=True,  # Ensures email uniqueness
        null=True,
        validators=[
            EmailValidator(message="Enter a valid email address.")
        ]
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensure email uniqueness validation beyond the database
        if Customer.objects.filter(email__iexact=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({"email": "A customer with this email already exists."})

    def save(self, *args, **kwargs):
        # Automatically convert email to lowercase before saving
        if self.email:
            self.email = self.email.lower()
        self.full_clean()  # Run clean to apply validation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Asset(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        PENDING_MAINTENANCE = 'Pending Maintenance', 'Pending Maintenance'
        DECOMMISSIONED = 'Decommissioned', 'Decommissioned'

    name = models.CharField(
        max_length=200,
        null=True,
        validators=[ 
            RegexValidator(
                regex=r'^(?=.*[a-zA-Z])(?=.*[a-zA-Z0-9]).+$',
                message="Asset name must contain at least one letter and cannot consist solely of special characters or numbers."
            )
        ]
    )
    assigned_to = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="assignment")
    warranty_expiry = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        null=False
    )
    description = models.CharField(
        max_length=450,
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(10, message="Description must be at least 10 characters, or left empty.")
        ]
    )
    date_assigned = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)  # Automatically updated when the asset is saved

    @property
    def is_warranty_pending(self):
        """Check if the asset's warranty has expired."""
        if self.warranty_expiry:
            return self.warranty_expiry >= date.today()
        return False

    @property
    def is_assigned(self):
        """Check if the asset is assigned to a customer."""
        return self.assigned_to is not None

    def __str__(self):
        return self.name
    

class MaintenanceHistory(models.Model):
    class MaintenanceType(models.TextChoices):
        REPAIR = 'Repair', 'Repair'
        SOFTWARE_UPDATE = 'Software Update', 'Software Update'
        CLEANING = 'Cleaning', 'Cleaning'
        OTHER = 'Other', 'Other'

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="maintenances")
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="maintenances")
    maintenance_type = models.CharField(max_length=50, choices=MaintenanceType.choices, null=False)
    description = models.TextField(
        null=True,
        blank=True,
        validators=[
            MinLengthValidator(10, message="Description must be at least 10 characters or left empty.")
        ]
    )
    date_maintained = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Maintenance: {self.asset.name} ({self.maintenance_type})"
