from django.urls import path
from .views import TimesheetList, TimesheetDetail,AllTimesheetList

urlpatterns = [
    path('', TimesheetList.as_view(), name='timesheet-list'),
    path('<int:pk>/', TimesheetDetail.as_view(), name='timesheet-detail'),
    path('all',AllTimesheetList.as_view(),name="All Time Sheet List")
]