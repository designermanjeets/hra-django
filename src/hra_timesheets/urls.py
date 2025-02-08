from django.urls import path
from .views import TimesheetList, TimesheetDetail

urlpatterns = [
    path('', TimesheetList.as_view(), name='timesheet-list'),
    path('<int:pk>/', TimesheetDetail.as_view(), name='timesheet-detail'),
]