from django.shortcuts import render
from ..models import Asset

def assets(request):
    assets = Asset.objects.all()
    return render(request, 'inventory/view-asset.html', {'assets': assets})
