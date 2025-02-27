from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from hra_bank_details.permissions import IsTenantUser
from .models import Timesheet
from .serializers import TimesheetSerializer
from hra_users.serializers import UserProfileSerializer
from hra_users.models import UserProfile
from hra_customers.views import check_user
import json
import base64


class AllTimesheetList(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_timesheet'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        timesheets = Timesheet.objects.filter(tenant_id=user_id.tenant_id.id)
        serializer = TimesheetSerializer(timesheets, many=True).data
        for i in serializer:
            i['timesheet_detail'] = json.loads(i['timesheet_detail'])
        return Response({"data":serializer,"message":"All TimeSheet Details","status":True},status=status.HTTP_200_OK)
    




class AddTimeSheet(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def post(self, request):

        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('add_timesheet'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        data['user_name'] = user_id.id
        data["tenant_id"] = user_id.tenant_id.id
        data['timesheet_detail'] = json.dumps(data['timesheet_detail'])
        base64_str = data['image']
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]
        

        decoded_image = base64.b64decode(base64_str)
        image_size_kb = len(decoded_image) / 1024  

        if image_size_kb > 500:
            return Response({"status": False, "message": "Image size should be less than 500KB."}, status=status.HTTP_400_BAD_REQUEST)

        serial = TimesheetSerializer(data = data)
        if serial.is_valid():
            serial.save()
            return Response({"status":True,"message":"Time Sheet added successfully","data":serial.data},status=status.HTTP_201_CREATED)
        else:
            return Response({"status":False,"message":serial.errors},status=status.HTTP_400_BAD_REQUEST)
        




class GetUserTimeSheet(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_timesheet'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        timesheets = Timesheet.objects.filter(user_name=user_id)
        serializer = TimesheetSerializer(timesheets, many=True).data
        for i in serializer:
            i['timesheet_detail'] = json.loads(i['timesheet_detail'])
        return Response({"data":serializer,"status":True,"message":"User TimeSheet Details"},status=status.HTTP_200_OK)
    




class ApproveDecliendTimeSheet(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def put(self,request,pk=None):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_timesheet'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        timesheet = get_object_or_404(Timesheet, timesheet_id=pk)
        if request.data.get('status') == '2' or request.data.get('status') == '3':
            timesheet.status = request.data.get('status')
            timesheet.save()
            message = "TimeSheet approved successfully" if request.data.get('status') == '2' else "TimeSheet declined successfully"
            return Response({"status":True,"message":message},status=status.HTTP_200_OK)
        else:
            return Response({"status":False,"message":"Invalid status"},status=status.HTTP_400_BAD_REQUEST)