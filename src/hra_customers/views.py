from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from hra_bank_details.permissions import IsTenantUser
from .models import Customer
from .serializers import CustomerSerializer
from hra_address.models import Address
from hra_address.serializers import AddressSerializer

class CustomerList(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        customers = Customer.objects.filter(tenant_id=request.user.tenant_id)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Extract address details from request
        billing_address_data = request.data.get("billing_address")
        shipping_address_data = request.data.get("shipping_address")
        
        # Create billing address
        billing_address_serializer = AddressSerializer(data=billing_address_data)
        if billing_address_serializer.is_valid():
            billing_address = billing_address_serializer.save()
        else:
            return Response(billing_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create shipping address
        shipping_address_serializer = AddressSerializer(data=shipping_address_data)
        if shipping_address_serializer.is_valid():
            shipping_address = shipping_address_serializer.save()
        else:
            return Response(shipping_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Add addresses to request data
        request.data["billing_address"] = billing_address.id
        request.data["shipping_address"] = shipping_address.id

        # Create customer
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant_id=request.user.tenant_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetail(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def get_object(self, pk):
        return get_object_or_404(Customer, pk=pk, tenant_id=self.request.user.tenant_id)

    def get(self, request, pk):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
