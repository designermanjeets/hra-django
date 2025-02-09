from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Address
from .serializers import AddressSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTenantUser
from rest_framework.renderers import JSONRenderer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class AddressList(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]  # Add JSONRenderer support

    def get(self, request):
        addresses = Address.objects.filter(tenant=request.user.tenant)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=AddressSerializer,
        operation_description="Create a new address",
        responses={
            201: 'Created',
            400: 'Bad Request',
        }

    )
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.user.tenant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddressDetail(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]  # Add JSONRenderer support

    def get_object(self, pk):
        return get_object_or_404(Address, pk=pk, tenant=self.request.user.tenant)

    def get(self, request, pk):
        address = self.get_object(pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        address = self.get_object(pk)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
