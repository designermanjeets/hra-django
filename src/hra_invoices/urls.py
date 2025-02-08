from django.urls import path
from .views import InvoiceList, InvoiceDetail

urlpatterns = [
    path('', InvoiceList.as_view(), name='invoice-list'),
    path('<int:pk>/', InvoiceDetail.as_view(), name='invoice-detail'),
]