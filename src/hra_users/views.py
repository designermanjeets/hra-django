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
        #usr = User.objects.create_user( )
        return Response({"stauts":True,"message":"success"},status=status.HTTP_201_CREATED)


class PermissionsApi(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self,request):
        data = request.data
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        data = Permission.objects.all()
        data = PermissionSerializer(data,many=True)
        return Response({"status":True,"message":"success","data":data.data},status=status.HTTP_200_OK)




