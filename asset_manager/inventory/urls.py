from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=''),
    path('assets/', views.assets, name='assets'),
    path('customer/', views.customer, name='customer'),

    path('login/', views.customer, name='login'),
    path('register/', views.customer, name='register'),
]