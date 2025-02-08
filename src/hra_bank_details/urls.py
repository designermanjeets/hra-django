from django.urls import path
from .views import BankDetailList, BankDetailDetail

urlpatterns = [
    path('bank-details/', BankDetailList.as_view(), name='bank-detail-list'),
    path('bank-details/<int:pk>/', BankDetailDetail.as_view(), name='bank-detail-detail'),
]