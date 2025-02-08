from django.urls import path
from .views import InvoiceList, InvoiceDetail

urlpatterns = [
    path('invoices/', InvoiceList.as_view(), name='invoice-list'),
    path('invoices/<int:pk>/', InvoiceDetail.as_view(), name='invoice-detail'),
]