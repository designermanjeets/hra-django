from django.urls import path
from .views import *

urlpatterns = [
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('emps',AllEmoloyes.as_view(),name="All Employees"),
    path('addEmp',AddEmp.as_view(),name="adding employee"),
    path("allpermissions",PermissionsApi.as_view(),name="all permissions")
    
] 