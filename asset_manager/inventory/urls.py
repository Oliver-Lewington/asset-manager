from django.urls import path
from .views.asset_views import assets
from .views.dashboard_views import dashboard
from .views.authentication_views import login, register, logout


urlpatterns = [
    path('', dashboard, name=''),
    path('assets/', assets, name='view-assets'),
    # path('customer/', x.customer, name='customer'),

    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
]