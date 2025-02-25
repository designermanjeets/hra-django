from django.urls import path
from .views import *

urlpatterns = [
    path('', PurchaseOrderList.as_view(), name='purchase-order-list'),
   
]