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

    # Make the asset field disabled (read-only) and set default for performed_by
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Disable the asset field
        if 'asset' in self.fields:
            self.fields['asset'].disabled = True

        # Disable the performed_by field for non-admin users and add a help text
        if 'performed_by' in self.fields:
            self.fields['performed_by'].disabled = True

            # Add conditional help text if the user is not staff (admin)
            if not kwargs.get('user', None) or not kwargs['user'].is_staff:
                self.fields['performed_by'].help_text = (
                    "You are unable to alter 'Performed By' field because you are not an admin."
                )
