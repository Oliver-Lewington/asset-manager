from django.shortcuts import render

def home(request):
    return render(request, 'inventory/dashboard.html')

def assets(request):
    pass

def customer(request):
    pass