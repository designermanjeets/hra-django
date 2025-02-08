from django.urls import path
from .views import PurchaseOrderList, PurchaseOrderDetail

urlpatterns = [
    path('po/', PurchaseOrderList.as_view(), name='purchase-order-list'),
    path('po/<int:pk>/', PurchaseOrderDetail.as_view(), name='purchase-order-detail'),
]