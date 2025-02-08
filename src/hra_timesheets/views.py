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

class TimesheetList(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        timesheets = Timesheet.objects.filter(user_name=request.user)
        serializer = TimesheetSerializer(timesheets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TimesheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_name=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimesheetDetail(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def get_object(self, pk):
        return get_object_or_404(Timesheet, pk=pk, user_name=self.request.user)

    def get(self, request, pk):
        timesheet = self.get_object(pk)
        serializer = TimesheetSerializer(timesheet)
        return Response(serializer.data)

    def put(self, request, pk):
        timesheet = self.get_object(pk)
        serializer = TimesheetSerializer(timesheet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        timesheet = self.get_object(pk)
        timesheet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
