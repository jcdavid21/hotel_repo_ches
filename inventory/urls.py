from django.urls import path
from . import views

urlpatterns = [
    # SPA Entry Point
    path('', views.inventory_spa, name='inventory_spa'),
    
    # API Endpoints
    path('api/items', views.api_inventory_items, name='api_items'),
    path('api/low-stock', views.api_low_stock, name='api_low_stock'),
    path('api/add', views.api_add_item, name='api_add'),
    path('api/update', views.api_update_stock, name='api_update'),
    path('api/remove', views.api_remove_item, name='api_remove'),
    path('api/request-cleaning', views.api_request_cleaning, name='api_request_cleaning'),
    path('api/request-restaurant', views.api_request_restaurant, name='api_request_restaurant'),
]
