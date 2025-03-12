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
        return Response({"status":True,"data":serializer.data,"message":"Purchase Order List"}, status=status.HTTP_200_OK)
    

class PurchaseOrderListByCustomer(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request,pk=None):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_purchaseorder'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
        purchase_orders = PurchaseOrder.objects.filter(customer_name=pk,tenant_id=request.user.tenant_id)
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response({"status":True,"data":serializer.data,"message":"Purchase Order List"}, status=status.HTTP_200_OK)




class AddPurchaseOrder(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('add_purchaseorder'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
        request.data['tenant_id'] = request.user.tenant_id.id   
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant_id=request.user.tenant_id)
            return Response({"status":True,"message":"Purchase order added successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status":False,"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class EditPurchaseOrder(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
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
        purchase_order = get_object_or_404(PurchaseOrder, purchase_order_id=pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(assigned_to=request.data.get('assigned_to'))
            return Response({"message":True,"data":serializer.data,"status":"Purchase order updated successfully"}, status=status.HTTP_200_OK)
        return Response({"status":False,"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





class AssignPurchaseOrderList(APIView):
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
        purchase_orders = [i.purchase_order_id for i in PurchaseOrder.objects.filter(tenant_id=request.user.tenant_id)]  
        assign_purchase_orders = AssignPurchaseOrder.objects.filter(purchase_order_id__in=purchase_orders)
        serializer = AssignPurchaseOrderSerializer(assign_purchase_orders, many=True)
        return Response({"status":True,"message":"Assign Purchase order list","data":serializer.data},status=status.HTTP_200_OK)

class Employeesassignorder(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request,pk=None):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_assignpurchaseorder'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
        purchase_orders = AssignPurchaseOrder.objects.filter(user_id=user_id.id)
    
        serializer = AssignPurchaseOrderSerializer(purchase_orders, many=True)
        return Response({"status":True,"data":serializer.data,"message":"Employee assign Order List"}, status=status.HTTP_200_OK)

    




    
    




class AddAssignPurchaseOrder(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        print(request.data.get('user_id'))
        if not user_profile.has_permission('add_assignpurchaseorder'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
        check = AssignPurchaseOrder.objects.filter(user_id=request.data.get("user_id"),status='1')
        if check:
            return Response({"status": False, "message": "Already assigned."}, status=status.HTTP_403_FORBIDDEN)
        serializer = AssignPurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"data":serializer.errors,"status":True,"message":"Assign successfully"}, status=status.HTTP_400_BAD_REQUEST)




class EditAssignPurchaseOrder(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
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
        assign_purchase_order = get_object_or_404(AssignPurchaseOrder, id=pk)
        serializer = AssignPurchaseOrderSerializer(assign_purchase_order, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(user_id=request.user)
            return Response(serializer.data)
        return Response({"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




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






