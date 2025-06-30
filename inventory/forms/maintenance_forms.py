from django import forms
from ..models import MaintenanceHistory, User

class MaintenanceHistoryForm(forms.ModelForm):
    class Meta:
        model = MaintenanceHistory
        fields = ['asset', 'performed_by', 'maintenance_type', 'description']

    performed_by = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Performed By',
        required=True  # Make this field required
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter maintenance description...',
            'rows': 3
            }),
        label='Description (Optional)'
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs and remove it from kwargs
        super().__init__(*args, **kwargs)

        # Disable the asset field
        if 'asset' in self.fields:
            self.fields['asset'].disabled = True

        # Handle the 'performed_by' field for non-admin users
        if 'performed_by' in self.fields:
            if not user or not user.is_staff:
                # Set the 'performed_by' field to the current user if not admin
                self.fields['performed_by'].initial = user
                self.fields['performed_by'].disabled = True  # Disable the field for non-admins
                self.fields['performed_by'].help_text = (
                    "You are unable to alter the 'Performed By' field because you are not an admin."
                )
