from django.contrib import messages
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from ..models import Asset, Customer
from ..forms.customer_forms import CustomerForm

from ..utils.shared_utils import redirect_when_next, staff_required
from ..utils.asset_utils import get_asset_assignments
from ..utils.customer_utils import get_filtered_customers, get_customer_metrics

# View all records
@login_required(login_url='login')
def view_customers(request):
    """
    Displays all customers with pagination and search functionality.
    Handles both regular requests.
    """
    search_query = request.GET.get('search', '')  # Get search query from URL params

    # Get filtered customers based on search query
    customers = get_filtered_customers(search_query)

    # Pagination: Show 5 customers per page
    paginator = Paginator(customers.order_by('-date_joined'), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate quick info metrics
    customer_metrics = get_customer_metrics(customers)
    asset_assignments = get_asset_assignments()


    context = {
        'page_obj': page_obj,
        'show_pagination': paginator.num_pages > 1,
        'customers_count': customers.count(),
        'search_query': search_query,  # Include search query in context
        **customer_metrics,  # Add customer metrics to context
        **asset_assignments
    }

    return render(request, 'inventory/customer/customers.html', context)

# View a single customer record
@login_required(login_url='login')
def view_customer(request, customer_id):
    """
    Displays detailed information for a single customer.
    Allows for editing or deletion of the customer.
    """
    customer = get_object_or_404(Customer, id=customer_id)

    # Retrieve all assets assigned to the customer
    assigned_assets = Asset.objects.filter(assigned_to=customer)

    form = CustomerForm(instance=customer)

    return render(request, 'inventory/customer/view-customer.html', {
        'customer': customer,
        'form': form,
        'assigned_assets': assigned_assets,  # Pass the assigned assets to the template
    })

# Create a new customer
@login_required(login_url='login')
def create_customer(request):
    """
    Displays the form to create a new customer. On form submission, saves the customer.
    """
    form = CustomerForm()

    if request.method == "POST":
        form = CustomerForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Customer has been created successfully.")
            return redirect_when_next(request,'view-customers')

    return render(request, 'inventory/customer/create-customer.html', {'form': form})

# Update an existing customer
@login_required(login_url='login')
def update_customer(request, customer_id):
    """
    Displays the form to update an existing customer. Saves changes upon form submission.
    """
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer record updated successfully.')
            return redirect_when_next(request, 'view-customer', customer_id=customer_id)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'inventory/customer/update-customer.html', {'form': form, 'customer_id': customer.id})

# Delete a customer
@staff_required
@login_required(login_url='login')
def delete_customer(request, customer_id):
    """
    Deletes a customer and redirects to the customer list page.
    """
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()

    messages.success(request, 'Customer record deleted successfully.')
    return redirect_when_next(request, 'view-customers')
