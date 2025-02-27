from django.urls import path
from .views import *

urlpatterns = [
    path('get', PurchaseOrderList.as_view(), name='purchase-order-list'),
    path('add' , AddPurchaseOrder.as_view(), name='purchase-order-list'),
    path("edit/<int:pk>", EditPurchaseOrder.as_view(), name='purchase-order-list'),
    path("assign-orders/get", AssignPurchaseOrderList.as_view(), name='purchase-order-list'),
    path("assign-orders/add", AddAssignPurchaseOrder.as_view(), name='purchase-order-list'),
    path("assign-orders/edit/<int:pk>", EditAssignPurchaseOrder.as_view(), name='purchase-order-list'),
   
]