from django.urls import path
from .views import *

urlpatterns = [
    path('', CustomerList.as_view(), name='customer-list'),
    path('add',AddCustomer.as_view(),name="add customer"),
    path('<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
]