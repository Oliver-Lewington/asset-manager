from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('assets/', views.assets, name='assets'),
    path('customer/', views.customer, name='customer'),
]