from django.urls import path
from .views import LookupList, LookupDetail

urlpatterns = [
    path('', LookupList.as_view(), name='lookup-list'),
    path('<int:pk>/', LookupDetail.as_view(), name='lookup-detail'),
]