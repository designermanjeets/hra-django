from django.urls import path
from . import views
from .views import AddressList, AddressDetail

urlpatterns = [
    path('address/', AddressList.as_view(), name='address-list'),
    path('address/<int:pk>/', AddressDetail.as_view(), name='address-detail'),
]
