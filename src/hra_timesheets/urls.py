from django.urls import path
from .views import TimesheetList, TimesheetDetail

urlpatterns = [
    path('timesheets/', TimesheetList.as_view(), name='timesheet-list'),
    path('timesheets/<int:pk>/', TimesheetDetail.as_view(), name='timesheet-detail'),
]