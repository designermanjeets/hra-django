from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Tenant
from rest_framework.renderers import JSONRenderer

# Create your views here.

class TenantListView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        tenants = Tenant.objects.all()
        # Add any additional logic here
        return Response({'tenants': tenants})

class TenantDetailView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get(self, request, tenant_id):
        try:
            tenant = Tenant.objects.get(id=tenant_id)
            # Add any additional logic here
            return Response({'tenant': tenant})
        except Tenant.DoesNotExist:
            return Response({'error': 'Tenant not found'}, status=404)

    def put(self, request, tenant_id):
        try:
            tenant = Tenant.objects.get(id=tenant_id)
            # Update the tenant object with request data
            # Add any additional logic here
            return Response({'message': 'Tenant updated successfully'})
        except Tenant.DoesNotExist:
            return Response({'error': 'Tenant not found'}, status=404)

    def delete(self, request, tenant_id):
        try:
            tenant = Tenant.objects.get(id=tenant_id)
            # Delete the tenant object
            # Add any additional logic here
            return Response({'message': 'Tenant deleted successfully'})
        except Tenant.DoesNotExist:
            return Response({'error': 'Tenant not found'}, status=404)