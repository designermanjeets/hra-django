from django.urls import path
from .views import ReportingManagerList, ReportingManagerDetail

urlpatterns = [
    path('reporting-managers/', ReportingManagerList.as_view(), name='reporting-manager-list'),
    path('reporting-managers/<int:pk>/', ReportingManagerDetail.as_view(), name='reporting-manager-detail'),
]