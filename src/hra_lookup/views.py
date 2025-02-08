from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Lookup
from .serializers import LookupSerializer
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer

class LookupList(generics.ListCreateAPIView):
    serializer_class = LookupSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            return Lookup.objects.filter(tenant_id=tenant_id)
        return Lookup.objects.all()

    def perform_create(self, serializer):
        tenant_id = self.request.data.get('tenant_id')
        serializer.save(tenant_id=tenant_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

class LookupDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LookupSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        tenant_id = self.request.query_params.get('tenant_id')
        if tenant_id:
            return Lookup.objects.filter(tenant_id=tenant_id)
        return Lookup.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)

