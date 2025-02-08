from django.urls import path
from .views import BankDetailList, BankDetailDetail

urlpatterns = [
    path('', BankDetailList.as_view(), name='bank-detail-list'),
    path('<int:pk>/', BankDetailDetail.as_view(), name='bank-detail-detail'),
]