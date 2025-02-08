from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from hra_bank_details.permissions import IsTenantUser
from .models import ReportingManager
from .serializers import ReportingManagerSerializer

class ReportingManagerList(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        reporting_managers = ReportingManager.objects.filter(tenant_id=request.user.tenant_id)
        serializer = ReportingManagerSerializer(reporting_managers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReportingManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant_id=request.user.tenant_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportingManagerDetail(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def get_object(self, pk):
        return get_object_or_404(ReportingManager, pk=pk, tenant_id=self.request.user.tenant_id)

    def get(self, request, pk):
        reporting_manager = self.get_object(pk)
        serializer = ReportingManagerSerializer(reporting_manager)
        return Response(serializer.data)

    def put(self, request, pk):
        reporting_manager = self.get_object(pk)
        serializer = ReportingManagerSerializer(reporting_manager, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reporting_manager = self.get_object(pk)
        reporting_manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)