from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from hra_bank_details.permissions import IsTenantUser
from .models import *
from .serializers import *
from hra_customers.views import check_user
from hra_users.models import UserProfile

class PurchaseOrderList(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_purchaseorder'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
     
        purchase_orders = PurchaseOrder.objects.filter(tenant_id=request.user.tenant_id)
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('add_purchaseorder'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
  
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant_id=request.user.tenant_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk=None):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_purchaseorder'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)   
        if pk is None:
            return Response({"status": False, "message": "Purchase Order ID is required."}, status=status.HTTP_400_BAD_REQUEST) 
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(assigned_to=request.data.get('assigned_to'))
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class AssignPurchaseOrder(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_assignpurchaseorder'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
        assign_purchase_orders = AssignPurchaseOrder.objects.filter(user_id=request.user)
        serializer = AssignPurchaseOrderSerializer(assign_purchase_orders, many=True)
        return Response(serializer.data)



    def post(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('add_assignpurchaseorder'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
        serializer = AssignPurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    def put(self,request,pk=None):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_assignpurchaseorder'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)   
        if pk is None:
            return Response({"status": False, "message": "Purchase Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        assign_purchase_order = self.get_object(pk)
        serializer = AssignPurchaseOrderSerializer(assign_purchase_order, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    






# class PurchaseOrderDetail(APIView):
#     permission_classes = [IsAuthenticated, IsTenantUser]
#     renderer_classes = [JSONRenderer]

#     def get_object(self, pk):
#         return get_object_or_404(PurchaseOrder, pk=pk, tenant_id=self.request.user.tenant_id)

#     def get(self, request, pk):
#         purchase_order = self.get_object(pk)
#         serializer = PurchaseOrderSerializer(purchase_order)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         purchase_order = self.get_object(pk)
#         serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
#         if serializer.is_valid():
#             serializer.save(assigned_to=request.data.get('assigned_to'))
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         purchase_order = self.get_object(pk)
#         purchase_order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)






