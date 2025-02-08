from django.urls import path
from . import views
from .views import TenantListView, TenantDetailView

urlpatterns = [
    path('', TenantListView.as_view(), name='tenant-list'),
    path('<int:tenant_id>/', TenantDetailView.as_view(), name='tenant-detail'),
]
