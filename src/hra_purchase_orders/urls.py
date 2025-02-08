from django.urls import path
from .views import PurchaseOrderList, PurchaseOrderDetail

urlpatterns = [
    path('', PurchaseOrderList.as_view(), name='purchase-order-list'),
    path('<int:pk>/', PurchaseOrderDetail.as_view(), name='purchase-order-detail'),
]