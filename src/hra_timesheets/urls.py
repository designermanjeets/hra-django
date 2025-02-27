from django.urls import path
from .views import *

urlpatterns = [
   
    path('all',AllTimesheetList.as_view(),name="All Time Sheet List"),
    path('add',AddTimeSheet.as_view(),name="Add Time Sheet"),
    path("get",GetUserTimeSheet.as_view(),name="Get User Time Sheet"),
    path("approve-decline/<int:pk>",ApproveDecliendTimeSheet.as_view(),name="Approve Decline Time Sheet")
]