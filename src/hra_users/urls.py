from django.urls import path
from .views import *

urlpatterns = [
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('emps',AllEmoloyes.as_view(),name="All Employees"),
    path('addEmp',AddEmp.as_view(),name="adding employee"),
    path("allpermissions",PermissionsApi.as_view(),name="all permissions"),
    path('api/roles/<int:pk>/assign_permissions', AssignPermissionsApi.as_view(), name='assign_permissions'),
    path('api/roles/<int:pk>/get_permissions', GetPermissionsApi.as_view(), name='get_permissions'),
    path('api/roles/add', AddRoleApi.as_view(), name='add_role'),
    path('api/roles/<int:pk>/edit', EditRoleApi.as_view(), name='disable_role'),
    path('api/roles', AllRolesApi.as_view(), name='All Roles'),
    path('api/permissions/<int:pk>/content_type', GetPermissionsById.as_view(), name='Get Permissions'),
] 