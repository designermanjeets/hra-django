from django.urls import path
from .views import CustomerList, CustomerDetail

urlpatterns = [
    path('', CustomerList.as_view(), name='customer-list'),
    path('<int:pk>/', CustomerDetail.as_view(), name='customer-detail'),
]