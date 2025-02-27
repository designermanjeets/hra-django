from django.urls import path
from .views import *

urlpatterns = [
    path("get",InvoiceList.as_view(),name="Invoice List"),
    path("add",AddInvoice.as_view(),name="Add Invoice"),
]