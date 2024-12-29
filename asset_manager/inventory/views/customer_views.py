from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Customer

@login_required(login_url='login')
def customers(request):
    customers = Customer.objects.all()
    return render(request, 'inventory/view-customer.html', {'customers': customers})
