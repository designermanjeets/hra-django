from django.urls import path
from .views import ReportingManagerList, ReportingManagerDetail

urlpatterns = [
    path('', ReportingManagerList.as_view(), name='reporting-manager-list'),
    path('<int:pk>/', ReportingManagerDetail.as_view(), name='reporting-manager-detail'),
]