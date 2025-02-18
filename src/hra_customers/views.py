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
from rest_framework_simplejwt.tokens import AccessToken
from hra_address.serializers import AddressSerializer
from django.contrib.auth import get_user_model
User = get_user_model()




def check_user(auth_header):
    
    if auth_header and auth_header.startswith("Bearer "):
        token_str = auth_header.split(" ")[1] 
        try:
            token = AccessToken(token_str)
            user_id = token["user_id"]  
            user_id = User.objects.get(id  = user_id)
            
        except Exception as e:
            return Response({"error": f"Invalid token: {str(e)}"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({"error": "Authorization token missing"}, status=status.HTTP_401_UNAUTHORIZED)
    return user_id






class CustomerList(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request,pk=None):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        
        
        customers = Customer.objects.filter(tenant_id=user_id.tenant_id.id)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    
    
class AddCustomer(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self,request):
        print("post request")
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        billing_address_data = request.data.get("billing_address")
        
        shipping_address_data = request.data.get("shipping_address")
        print(billing_address_data)
        
        
        billing_address_serializer = AddressSerializer(data=billing_address_data)
        if billing_address_serializer.is_valid():
            billing_address = billing_address_serializer.save()
        else:
            return Response(billing_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print("biiling Saved successfully")

        shipping_address_serializer = AddressSerializer(data=shipping_address_data)
        if shipping_address_serializer.is_valid():
            shipping_address = shipping_address_serializer.save()
        else:
            return Response(shipping_address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        request.data["billing_address"] = billing_address.id
        request.data["shipping_address"] = shipping_address.id
        request.data['tenant_id'] = user_id.tenant_id.id
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"status":True,"message":"success"}, status=status.HTTP_201_CREATED)
        return Response({"status":False,"message":"Failed","error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def get_object(self, pk=None):
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
