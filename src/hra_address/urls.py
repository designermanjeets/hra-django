from django.urls import path
from . import views
from .views import AddressList, AddressDetail

urlpatterns = [
    path('', AddressList.as_view(), name='address-list'),
    path('<int:pk>/', AddressDetail.as_view(), name='address-detail'),
]
