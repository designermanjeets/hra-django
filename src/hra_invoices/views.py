from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from hra_bank_details.permissions import IsTenantUser
from .models import Invoice
from .serializers import InvoiceSerializer,InvoiceItemSerializer
from hra_customers.views import check_user
from hra_users.models import UserProfile
import time





class InvoiceList(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_empdetail'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
        invoices = Invoice.objects.filter(tenant_id=request.user.tenant_id)
        serializer = InvoiceSerializer(invoices, many=True) 
        return Response({"status":True,"data":serializer.data,"message":"Invoice List"}, status=status.HTTP_200_OK)
    






class AddInvoice(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        data = request.data
        if not user_profile.has_permission('change_empdetail'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)   
        data['tenant_id'] = request.user.tenant_id.id
        data["order_number"] = int(time.time())
        data["invoice_number"] = int(time.time())
        serializer = InvoiceSerializer(data=data)
        if serializer.is_valid():
            invoice_id = serializer.save(tenant_id=request.user.tenant_id)
            for i in data['invoice_items']:
                i['invoice'] = invoice_id.invoice_id
                serializer1 = InvoiceItemSerializer(data=i)
                if serializer1.is_valid():
                    serializer1.save()
                else:
                    return Response({"status":False,"error":serializer1.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status":True,"message":"Invoice added successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status":False,"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
    

