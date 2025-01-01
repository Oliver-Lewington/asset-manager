from django.urls import path

from .views import asset_views
from .views import maintainance_views
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
    path('maintenance/create/', maintainance_views.update_maintenance, name='create-maintenance'),
    path('maintenance/update/<int:maintenance_id>/', maintainance_views.update_maintenance, name='update-maintenance'),
    path('maintenance/delete/<int:maintenance_id>/', maintainance_views.delete_maintenance, name='delete-maintenance'),

    path('customers/', customers, name='customers'),

    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),    
]