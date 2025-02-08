from django.urls import path
from . import views
from .views import TenantListView, TenantDetailView

urlpatterns = [
    path('tenants/', TenantListView.as_view(), name='tenant-list'),
    path('tenants/<int:tenant_id>/', TenantDetailView.as_view(), name='tenant-detail'),
]
