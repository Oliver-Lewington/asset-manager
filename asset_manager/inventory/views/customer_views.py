from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from ..models import Asset, Customer
from ..forms.customer_forms import CustomerForm

# View all records
@login_required(login_url='login')
def view_customers(request):
    """
    Displays all customers with pagination and search functionality.
    Handles both AJAX and regular requests.
    """

    search_query = request.GET.get('search', '')

    # Filter customers based on search query
    customers = Customer.objects.filter(
        Q(name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(phone_number__icontains=search_query)
    )

    # Pagination: Show 5 customers per page
    paginator = Paginator(customers.order_by('-date_joined'), 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    show_pagination = paginator.num_pages > 1

    # Check if pagination is needed
    show_pagination = paginator.num_pages > 1

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Handle AJAX requests
        # Prepare customer data for AJAX response
        customer_data = [{
            'id': customer.id,
            'name': customer.name,
            'phone_number': customer.phone_number,
            'email': customer.email,
            'date_joined': customer.date_joined
        } for customer in page_obj.object_list]

        return JsonResponse({
            'customers': customer_data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'num_pages': paginator.num_pages,
        })

    # Quick Info Metrics
    total_customers = customers.count()
    customers_with_assets = Customer.objects.annotate(asset_count=Count('assignment')).filter(asset_count__gt=0).count()
    customers_without_assets = total_customers - customers_with_assets
    unassigned_assets = Asset.objects.filter(assigned_to__isnull=True).count()

    context = {
        'page_obj': page_obj,
        'show_pagination': show_pagination,
        'total_customers': total_customers,
        'customers_with_assets': customers_with_assets,
        'customers_without_assets': customers_without_assets,
        'unassigned_assets': unassigned_assets,
        'search_query': search_query,
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
            return redirect('view-customers')

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
            return redirect('view-customer', customer_id=customer_id)
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'inventory/customer/update-customer.html', {'form': form})


# Delete a customer
@login_required(login_url='login')
def delete_customer(request, customer_id):
    """
    Deletes a customer and redirects to the customer list page.
    """
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()

    messages.success(request, 'Customer record deleted successfully.')
    return redirect('view-customers')
