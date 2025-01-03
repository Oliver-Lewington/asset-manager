from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from ..forms.asset_forms import AssetForm
from ..models import Asset, MaintenanceHistory
from ..utils.shared_utils import redirect_when_next
from ..utils.asset_utils import get_filtered_assets, get_asset_metrics, get_asset_by_id

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
    paginator = Paginator(assets.order_by('-last_updated'), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate quick info metrics
    asset_metrics = get_asset_metrics(assets)

    context = {
        'page_obj': page_obj,
        'show_pagination': paginator.num_pages > 1,
        'assets_count': assets.count(),
        'search_query': search_query,  # Include search query in context
        **asset_metrics,  # Add asset metrics to context
    }

    return render(request, 'inventory/asset/assets.html', context)



# View a single asset record
@login_required(login_url='login')
def view_asset(request, asset_id):
    """
    Displays detailed information for a single asset, including maintenance history.
    Allows for editing or deletion of the asset.
    """
    asset = get_asset_by_id(asset_id)

    # Fetch maintenance history related to the asset
    maintenance_history = MaintenanceHistory.objects.filter(asset=asset).order_by('-date_maintained')

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
            return redirect_when_next(request, 'view-assets')

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
            return redirect_when_next(request, 'view-asset', asset_id=asset_id)
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
    return redirect_when_next(request, 'view-assets')  # Redirect to 'view-assets' if no 'next' param