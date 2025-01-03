from django.urls import path

from .views import asset_views
from .views import maintenance_views
from .views import customer_views
from .views.dashboard_views import dashboard
from .views import authentication_views

urlpatterns = [
    path('', dashboard, name=''),

    # - Asset URLs
    path('assets/', asset_views.view_assets, name='view-assets'),
    path('assets/<int:asset_id>/', asset_views.view_asset, name='view-asset'),
    path('assets/create', asset_views.create_asset, name='create-asset'),
    path('assets/update/<int:asset_id>/', asset_views.update_asset, name='update-asset'),
    path('assets/delete/<int:asset_id>/', asset_views.delete_asset, name='delete-asset'),
     
    # - Maintenance History URLs
    # When creating a maintenance record, the asset must be bound to the maintenance automatically.
    path('maintenance/create/<int:asset_id>', maintenance_views.create_maintenance, name='create-maintenance'),
    path('maintenance/update/<int:maintenance_id>/', maintenance_views.update_maintenance, name='update-maintenance'),
    path('maintenance/delete/<int:maintenance_id>/', maintenance_views.delete_maintenance, name='delete-maintenance'),

    # - Customer URLs
    path('customers/', customer_views.view_customers, name='view-customers'),
    path('customers/create', customer_views.create_customer, name='create-customer'),
    path('customers/<int:customer_id>/', customer_views.view_customer, name='view-customer'),
    path('customers/update/<int:customer_id>/', customer_views.update_customer, name='update-customer'),
    path('customers/delete/<int:customer_id>/', customer_views.delete_customer, name='delete-customer'),

    # - User Management/Authorization URLs
    path('login/', authentication_views.login, name='login'),
    path('logout/', authentication_views.logout, name='logout'),    
    path('register/', authentication_views.register, name='register'),
    path('delete-account/', authentication_views.delete_account, name='delete-account')
]