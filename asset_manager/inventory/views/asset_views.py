from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from ..utils.asset_utils import get_filtered_assets, get_asset_metrics
from ..models import Asset, MaintenanceHistory
from ..forms.asset_forms import AssetForm

# View all records
@login_required(login_url='login')
def view_assets(request):
    """
    Displays all assets with pagination and search functionality.
    Handles both AJAX and regular requests.
    """
    search_query = request.GET.get('search', '')  # Get search query from URL params

    # Get filtered assets based on search query
    assets = get_filtered_assets(search_query)

    # Pagination: Show 5 assets per page
    paginator = Paginator(assets.order_by('-date_assigned'), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if pagination is needed
    show_pagination = paginator.num_pages > 1

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Handle AJAX requests
        # Prepare asset data for AJAX response
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

    # Calculate quick info metrics
    asset_metrics = get_asset_metrics(assets)

    context = {
        'page_obj': page_obj,
        'show_pagination': show_pagination,
        'assets_count': assets.count(),
        **asset_metrics,  # Add asset metrics to context
        'search_query': search_query,
    }

    return render(request, 'inventory/asset/assets.html', context)


# View a single asset record
@login_required(login_url='login')
def view_asset(request, asset_id):
    """
    Displays detailed information for a single asset, including maintenance history.
    Allows for editing or deletion of the asset.
    """
    asset = get_object_or_404(Asset, id=asset_id)

    # Fetch maintenance history related to the asset
    maintenance_history = MaintenanceHistory.objects.filter(asset=asset).order_by('-date_maintained')

    # Handle asset deletion
    if request.method == 'POST' and 'delete_asset' in request.POST:
        asset.delete()
        messages.success(request, 'Asset deleted successfully.')
        return redirect('asset_list')  # Redirect to asset list view after deletion

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


# Create a new asset
@login_required(login_url='login')
def create_asset(request):
    """
    Displays the form to create a new asset. On form submission, saves the asset.
    """
    form = AssetForm()

    if request.method == "POST":
        form = AssetForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your Asset has been created successfully.")
            return redirect('view-assets')

    return render(request, 'inventory/asset/create-asset.html', {'form': form})


# Update an existing asset
@login_required(login_url='login')
def update_asset(request, asset_id):
    """
    Displays the form to update an existing asset. Saves changes upon form submission.
    """
    asset = get_object_or_404(Asset, id=asset_id)

    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset record updated successfully.')
            return redirect('view-asset', asset_id=asset_id)
    else:
        form = AssetForm(instance=asset)

    return render(request, 'inventory/asset/update-asset.html', {'form': form})


# Delete an asset
@login_required(login_url='login')
def delete_asset(request, asset_id):
    """
    Deletes an asset and redirects to the asset list page.
    """
    asset = get_object_or_404(Asset, id=asset_id)
    asset.delete()

    messages.success(request, 'Asset record deleted successfully.')
    return redirect('view-assets')