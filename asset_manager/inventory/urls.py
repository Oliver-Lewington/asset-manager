from django.urls import path

from .views import asset_views
from .views import maintenance_views
from .views.customer_views import customers
from .views.dashboard_views import dashboard
from .views.authentication_views import login, register, logout

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

    path('customers/', customers, name='customers'),

    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),    
]