from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import *
from rest_framework.renderers import JSONRenderer
from hra_customers.views import check_user
from hra_bank_details.permissions import IsTenantUser
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password






class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get_object(self):
        return self.request.user




class AllEmoloyes(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request,pk=None):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_empdetail'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        customers = User.objects.filter(tenant_id=user_id.tenant_id.id,job_role='emp')
        serializer = UserSerializer(customers, many=True)
        return Response({"data":serializer.data,"status":True,"message":"success"},status=status.HTTP_200_OK)
 





class AddEmp(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self,request):
        data = request.data
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('add_empdetail'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)

        data['tenant_id'] = user_id.tenant_id.id
        data['password'] = make_password(data["password"])

        user_serial = UserSerializer(data=data)
        if user_serial.is_valid():
            usr = user_serial.save()
            usr = usr.id
        else:
            return Response({"status":False,"message":"Failed","errors":user_serial.errors},status=status.HTTP_400_BAD_REQUEST)

        profile_data = {"user":usr,"role":Role.objects.get(name=data["job_role"])}
        profile_serial = UserProfileSerializer(profile_data)
        if profile_serial.is_valid():
            profile_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":profile_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        



                    
                        
        return Response({"stauts":True,"message":"success"},status=status.HTTP_201_CREATED)




class PermissionsApi(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self,request):
        data = request.data
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_permission'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN )
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        data = Permission.objects.all()
        data = PermissionSerializer(data,many=True)
        return Response({"status":True,"message":"success","data":data.data},status=status.HTTP_200_OK)





class AssignPermissionsApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_permission'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        permission_ids = request.data.get('permissions', [])
        permissions = Permission.objects.filter(id__in=permission_ids)
        role.permissions.set(permissions)
        return Response({"status": True, "message": "Permissions assigned successfully"}, status=status.HTTP_200_OK)
    


class GetPermissionsApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_permission'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        permissions = role.permissions.all()
        data = PermissionSerializer(permissions, many=True)
        return Response({"status": True, "message": "success", "data": data.data}, status=status.HTTP_200_OK)




class AddRoleApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('add_role'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Role added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

  
class EditRoleApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self, request, pk):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_role'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
      
        role = get_object_or_404(Role, pk=pk)
        serial = RoleSerializer(role,data=request.data,partial=True)
        if serial.is_valid():
            serial.save()
       
            return Response({"status": True, "message": "success"}, status=status.HTTP_200_OK)
        else:

            return Response({"status": False, "message": "Failed","error":serial.errors}, status=status.HTTP_400_BAD_REQUEST)



class AllRolesApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_role'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response({"status": True, "message": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    


class GetPermissionsById(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request,pk=None):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_permission'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        permissions = Permission.objects.filter(content_type=pk)
        serial = PermissionSerializer(permissions,many=True)
        return Response({"status": True, "message": "success", "data": serial.data}, status=status.HTTP_200_OK)