from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from datetime import date

from ..models import Asset, MaintenanceHistory
from ..forms.asset_forms import AssetForm, CreateAssetForm, UpdateAssetForm

# - View all record
@login_required(login_url='login')
def view_assets(request):
    search_query = request.GET.get('search', '')  

    # Filter assets based on the search query
    assets = Asset.objects.filter(name__icontains=search_query) if search_query else Asset.objects.all()
    
    # Pagination: Show 5 assets per page
    paginator = Paginator(assets.order_by('-date_assigned'), 5)
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    # Determine if pagination is necessary
    show_pagination = paginator.num_pages > 1

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check for AJAX requests
        # Return JSON for real-time search
        asset_data = [{
            'id': asset.id,
            'name': asset.name,
            'status': asset.status,
            'warranty': 'Valid' if asset.is_warranty_pending else 'Expired',
        } for asset in page_obj.object_list]
        return JsonResponse({
            'assets': asset_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'num_pages': paginator.num_pages,
        })

    # Quick info metrics
    active_assets = assets.filter(status=Asset.StatusChoices.ACTIVE).count()
    maintenance_assets = assets.filter(status=Asset.StatusChoices.PENDING_MAINTENANCE).count()
    decommissioned_assets = assets.filter(status=Asset.StatusChoices.DECOMMISSIONED).count()
    assets_under_warranty = assets.filter(warranty_expiry__gte=date.today()).count()
    assets_out_of_warranty = assets.filter(warranty_expiry__lt=date.today()).count()

    context = {
        'page_obj': page_obj,
        'show_pagination': show_pagination,
        'assets_count': assets.count(),
        'active_assets': active_assets,
        'maintenance_assets': maintenance_assets,
        'decommissioned_assets': decommissioned_assets,
        'assets_under_warranty': assets_under_warranty,
        'assets_out_of_warranty': assets_out_of_warranty,
        'search_query': search_query,
    }
    return render(request, 'inventory/asset/assets.html', context)

# - View a record
@login_required(login_url='login')
def view_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    
    # Fetch maintenance history related to the asset
    maintenance_history = MaintenanceHistory.objects.filter(asset=asset).order_by('-date_maintained')

    # Handle asset deletion
    if request.method == 'POST' and 'delete_asset' in request.POST:
        asset.delete()
        messages.success(request, 'Asset deleted successfully.')
        return redirect('asset_list')  # Redirect to your asset list view after deletion

    # Handle asset edit
    if request.method == 'POST' and 'edit_asset' in request.POST:
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset updated successfully.')
            return redirect('asset_detail', asset_id=asset.id)
    else:
        form = AssetForm(instance=asset)

    return render(request, 'inventory/asset/view-asset.html', {
        'asset': asset,
        'maintenance_history': maintenance_history,
        'form': form,
    })

# - Create a record
@login_required(login_url='login')
def create_asset(request):
    form = CreateAssetForm()

    if request.method == "POST":
        form = CreateAssetForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your Asset has been created successfully.")
            return redirect('view-assets')
        
    context = { 'form':form }

    return render(request, 'inventory/asset/create-asset.html', context = context)

# - Update a record
login_required(login_url='login')
def update_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    
    # Handle maintenance edit
    if request.method == 'POST':
        form = UpdateAssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset record updated successfully.')
            return redirect('view-asset', asset_id=asset_id)
    else:
        form = UpdateAssetForm(instance=asset)

    return render(request, 'inventory/asset/update-asset.html', {'form': form})

# - Update a record
@login_required(login_url='login')
def delete_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    asset.delete()

    messages.success(request, F'Asset record deleted successfully.')
    
    return redirect('view-assets')
