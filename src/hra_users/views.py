from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import *
from rest_framework.renderers import JSONRenderer
from hra_customers.views import check_user
from hra_bank_details.permissions import IsTenantUser
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
import random
import time
from django.contrib.auth.hashers import make_password
from hra_bank_details.models import *
from hra_bank_details.serializers import *




def store_activity(data):

    serial = ActivityLogsSerializer(data=data)
    if serial.is_valid():
        serial.save()
        return True
    else:
        return serial.errors

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def get_object(self):
        return self.request.user
    




class ChangeStatusUser(APIView):
    def put(self, request,pk=None):

        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_empdetail'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
        if pk is not None:
            user = get_object_or_404(User, id=pk)
            user.status = request.data.get('status')
            user.save()
            message  = "User enabled successfully" if user.status == 'Active' else "User disabled successfully"
            activity_logs={ "user":user_id.id,"name":"Change Status","status":"1","table":"User","action":"Put Request","message":message}
            activity = store_activity(activity_logs)
            return Response({"status":True,"message":message},status=status.HTTP_200_OK)
        else:
            return Response({"status":False,"message":"Employee not found"},status=status.HTTP_404_NOT_FOUND)








class EditEmployee(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def put(self, request,pk=None):

        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_empdetail'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)    
        if pk is None:
            return Response({"status":False,"message":"Employee not found"},status=status.HTTP_404_NOT_FOUND)
        



        try:
            data = request.data
            user = get_object_or_404(User, id=pk)
            user_serial = UserSerializer(user,data=data,partial=True)
        except:
            return Response({"status":False,"message":"Employee not found"},status=status.HTTP_404_NOT_FOUND)
        if user_serial.is_valid():
            user_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":user_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        

        

        profile_data = {"user":pk,"role":Role.objects.get(name=data["job_role"]).id}
        profile = get_object_or_404(UserProfile, user_id=pk)
        profile_serial = UserProfileSerializer(profile,data=profile_data,partial=True)
        if profile_serial.is_valid():
            profile_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":profile_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        

        



        emp = get_object_or_404(EmpDetail, user=pk)
        emp_serial = EmpDetailSerializer(emp,data=data,partial=True)
        if emp_serial.is_valid():
            emp_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":emp_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        



        
        personal_detail = get_object_or_404(PersonalDetail, emp_id=emp.id)
        personal_serial = PersonalDetailSerializer(personal_detail,data=data.get("personal_detail"),partial=True)
        if personal_serial.is_valid():
            personal_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":personal_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        

        

        bank_detail = get_object_or_404(BankDetail, user=pk)
        bank_serial = BankDetailSerializer(bank_detail,data=data.get("bank_detail"),partial=True)
        if bank_serial.is_valid():
            bank_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":bank_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        

        
        
        address_detail = get_object_or_404(AddressDetail, emp_id=emp.id)
        address_serial = AddressDetailSerializer(address_detail,data=data.get("address_detail"),partial=True)
        if address_serial.is_valid():
            address_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":address_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        

        

        visa_detail = get_object_or_404(Visadetail, emp_id=emp.id)
        visa_serial = VisadetailSerializer(visa_detail,data=data.get("visa_detail"),partial=True)
        if visa_serial.is_valid():
            visa_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":visa_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        


        
        education = data.get('education')
        for i in education:
            if i.get("id") is not None:
                edu = get_object_or_404(Education, id=i["id"])
                edu_serial = EducationSerializer(edu,data=i,partial=True)
                if edu_serial.is_valid():
                    edu_serial.save()
                else:
                    return Response({"status":False,"message":"Failed","errors":edu_serial.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                i["emp_id"]=emp.id
                edu_serial = EducationSerializer(data=i)
                if edu_serial.is_valid():
                    edu_serial.save()
                else:
                    return Response({"status":False,"message":"Failed","errors":edu_serial.errors},status=status.HTTP_400_BAD_REQUEST)
                



        experience = data.get('experience')
        for i in experience:
            if i.get("id") is not None:
                exp = get_object_or_404(Experience, id=i["id"])
                exp_serial = ExperienceSerializer(exp,data=i,partial=True)
                if exp_serial.is_valid():
                    exp_serial.save()
                else:
                    return Response({"status":False,"message":"Failed","errors":exp_serial.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                i["emp_id"]=emp.id
                exp_serial = ExperienceSerializer(data=i)
                if exp_serial.is_valid():
                    exp_serial.save()
                else:
                    return Response({"status":False,"message":"Failed","errors":exp_serial.errors},status=status.HTTP_400_BAD_REQUEST)
                


        return Response({"status":True,"message":"Employee updated successfully"},status=status.HTTP_200_OK)
        


        





class AllEmoloyes(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request,pk=None):

        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_empdetail'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        

        if pk is None:
            users = User.objects.filter(tenant_id=user_id.tenant_id.id,job_role='emp')
        
            user_data = UserSerializer(users, many=True).data
            activity_logs={
                "user":user_id.id,"name":"Get all Employees","status":"1","table":"Employee","action":"Get Request","message":"get all employees"
                           }
            activity = store_activity(activity_logs)
            for i in user_data:
                try:
                    user_profile = EmpDetail.objects.get(user=i["id"])
                    i["profile"]=EmpDetailSerializer(user_profile).data
                except:
                    i["profile"]={}
                try:
                    bank_detail = BankDetail.objects.get(user=i["id"])
                    i["bank_detail"]=BankDetailSerializer(bank_detail).data
                except:
                    i["bank_detail"]={}
            return Response({"data":user_data,"status":True,"message":"All Employee data"},status=status.HTTP_200_OK)
        else:

            try:
                users = User.objects.get(id=pk)
                user_data = UserSerializer(users).data
                print("User data-------->",user_data)
                activity_logs={
                    "user":user_id.id,"name":"Get Employee by id","status":"1","table":"Employee","action":"Get Request","message":f"get  employees username : {users.username}"
                             }
                activity = store_activity(activity_logs)
            except:
                return Response({"status":False,"message":"Employee not found"},status=status.HTTP_404_NOT_FOUND)
            try:
                user_profile = EmpDetail.objects.get(user=user_data["id"])
                user_data["profile"]=EmpDetailSerializer(user_profile).data
            except:
                user_data["profile"]={}
            try:
                bank_detail = BankDetail.objects.get(user=user_data["id"])
                user_data["bank_detail"]=BankDetailSerializer(bank_detail).data
            except:
                user_data["bank_detail"]={}
            print("user_data-------->",user_data)

            try:
                personal_detail = PersonalDetail.objects.get(emp_id=user_profile.id)
                user_data["personal_detail"]=PersonalDetailSerializer(personal_detail).data
            except:
                user_data["personal_detail"]={}
            try:
                address_detail = AddressDetail.objects.get(emp_id=user_profile.id)
                user_data["address_detail"]=AddressDetailSerializer(address_detail).data
            except:
                user_data["address_detail"]={}
            try:
                visa_detail = Visadetail.objects.get(emp_id=user_profile.id)
                user_data["visa_detail"]=VisadetailSerializer(visa_detail).data
            except:
                user_data["visa_detail"]={}
            try:
                education = Education.objects.filter(emp_id=user_profile.id)
                user_data["education"]=EducationSerializer(education,many=True).data
            except:
                user_data["education"]=[]
            try:
                experience = Experience.objects.filter(emp_id=user_profile.id)
                user_data["experience"]=ExperienceSerializer(experience,many=True).data
            except:
                user_data["experience"]=[]
            
            return Response({"data":user_data,"status":True,"message":"Employee data"},status=status.HTTP_200_OK)


            





class AddEmp(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self,request):


        data = request.data
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)



        if not user_profile.has_permission('add_empdetail'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        


        data['tenant_id'] = user_id.tenant_id.id
        data['password'] = make_password(data["password"])
        user_serial = UserSerializer(data=data)
        if user_serial.is_valid():
            usr = user_serial.save()
            usr = usr.id
        else:
            return Response({"status":False,"message":"Failed","errors":user_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        

        print("user data success")


        profile_data = {"user":usr,"role":Role.objects.get(name=data["job_role"]).id}
        profile_serial = UserProfileSerializer(data=profile_data)
        if profile_serial.is_valid():
            profile_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":profile_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        

        print("profile data success")
        
        data['user']=usr
        data["emp_code"]= "EMP"+str(int(time.time()))
        emp_serial = EmpDetailSerializer(data=data)
        if emp_serial.is_valid():
            emp_id=emp_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":emp_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        print("emp data success")





        personal_detail=data.get("personal_detail")
        personal_detail["emp_id"]=emp_id.id
        personal_serial = PersonalDetailSerializer(data=personal_detail)
        if personal_serial.is_valid():
            personal_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":personal_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        
        print("personal data success")


        address_detail=data.get("address_detail")
        address_detail["emp_id"]=emp_id.id
        address_serial = AddressDetailSerializer(data=address_detail)
        if address_serial.is_valid():
            address_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":address_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        

        print("address data success")
        visa_detail=data.get("visa_detail")
        visa_detail["emp_id"]=emp_id.id
        visa_serial = VisadetailSerializer(data=visa_detail)
        if visa_serial.is_valid():
            visa_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":visa_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        

        print("visa data success")
        
        
        bank_detail = data.get("bank_detail")
        bank_detail["user"]=usr
        bank_serial = BankDetailSerializer(data=bank_detail)
        if bank_serial.is_valid():
            bank_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":bank_serial.errors},status=status.HTTP_400_BAD_REQUEST)
        

        
        print("bank data success")
        education = []
        for i in data.get("education"):
            i["emp_id"]=emp_id.id
            education.append(i)
        education_serial = EducationSerializer(data=education,many=True)
        if education_serial.is_valid():
            education_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":education_serial.errors},status=status.HTTP_400_BAD_REQUEST)        
        print("education data success")

        experience = []
        for i in data.get("experience"):
            i["emp_id"]=emp_id.id
            experience.append(i)

        experience_serial = ExperienceSerializer(data=experience,many=True)
        if experience_serial.is_valid():
            experience_serial.save()
        else:
            return Response({"status":False,"message":"Failed","errors":experience_serial.errors},status=status.HTTP_400_BAD_REQUEST) 
        print("experience data success")

        return Response({"status":True,"message":"employee created successfully"},status=status.HTTP_201_CREATED)




class PermissionsApi(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self,request):
        data = request.data
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_permission'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN )
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        data = Permission.objects.all()
        data = PermissionSerializer(data,many=True)
        activity_logs={
            "user":user_id.id,"name":"Get all Permissions","status":"1","table":"Permissions","action":"Get Request","message":"get all permissions"
                       }
        activity = store_activity(activity_logs)
        return Response({"status":True,"message":"success","data":data.data},status=status.HTTP_200_OK)





class AssignPermissionsApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_permission'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        permission_ids = request.data.get('permissions', [])
        permissions = Permission.objects.filter(id__in=permission_ids)
        role.permissions.set(permissions)
        return Response({"status": True, "message": "Permissions assigned successfully"}, status=status.HTTP_200_OK)
    


class GetPermissionsApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request, pk):
        role = get_object_or_404(Role, pk=pk)
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_permission'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        permissions = role.permissions.all()
        data = PermissionSerializer(permissions, many=True)
        activity_logs={
            "user":user_id.id,"name":"Get all Permissions","status":"1","table":"Permissions","action":"Get Request","message":"get all permissions"
                       }
        activity = store_activity(activity_logs)
        return Response({"status": True, "message": "success", "data": data.data}, status=status.HTTP_200_OK)




class AddRoleApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('add_role'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            activity_logs={
            "user":user_id.id,"name":"Role Added","status":"1","table":"Roles","action":"Post Request","message":f"Role added {request.data.get("name")}"
                       }
            activity = store_activity(activity_logs)
            return Response({"status": True, "message": "Role added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

  
class EditRoleApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self, request, pk):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_role'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
      
        role = get_object_or_404(Role, pk=pk)
        serial = RoleSerializer(role,data=request.data,partial=True)
        activity_logs={
            "user":user_id.id,"name":"Edit Role","status":"1","table":"Roles","action":"put Request","message":f"Edit Role"
                       }
        activity = store_activity(activity_logs)
        if serial.is_valid():
            serial.save()
            return Response({"status": True, "message": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "message": "Failed","error":serial.errors}, status=status.HTTP_400_BAD_REQUEST)



class AllRolesApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_role'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        activity_logs={
            "user":user_id.id,"name":"Get all Roles","status":"1","table":"Roles","action":"Get Request","message":"get all Roles"
                       }
        activity = store_activity(activity_logs)
        return Response({"status": True, "message": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    


class GetPermissionsById(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request,pk=None):      
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_permission'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        permissions = Permission.objects.filter(content_type=pk)
        serial = PermissionSerializer(permissions,many=True)
        activity_logs={
            "user":user_id.id,"name":"Get permissions","status":"1","table":"Permission","action":"Get Request","message":f"get permissions by id"
                       }
        activity = store_activity(activity_logs)

        return Response({"status": True, "message": "success", "data": serial.data}, status=status.HTTP_200_OK)
    


class changeEmployeePassword(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def post(self, request):
        data = request.data
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_user'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, id=data.get("id"))
        if data.get("new_password") == data.get("confirm_password"):
            user.set_password(data["new_password"])
            user.save()
            return Response({"status": True, "message": "Password changed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "message": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)



class GetJobRoleApi(APIView):
    permission_classes = [IsAuthenticated,IsTenantUser]
    renderer_classes = [JSONRenderer]
    def get(self, request):
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('view_jobrole'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        roles = JobRole.objects.all()
        serializer = JobRoleSerializer(roles, many=True)
        activity_logs={
            "user":user_id.id,"name":"Get Job Roles","status":"1","table":"Roles","action":"Get Request","message":"get all Job Roles"
                       }
        activity = store_activity(activity_logs)
        return Response({"status": True, "message": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    def post(self,request):
        data = request.data
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('add_jobrole'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        serializer = JobRoleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            activity_logs={
            "user":user_id.id,"name":"Add Job Role","status":"1","table":"Roles","action":"Post Request","message":f"Role added {request.data.get("name")}"
                       }
            activity = store_activity(activity_logs)
            return Response({"status": True, "message": "Role added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def put(self,request):
        data = request.data
        auth_header = request.headers.get('Authorization', None)
        user_id = check_user(auth_header)
        user_profile = get_object_or_404(UserProfile, user_id=user_id)
        if not user_profile.has_permission('change_jobrole'):
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        elif user_profile.role.status !='1':
            return Response({"status": False, "message": "Have no permission."}, status=status.HTTP_403_FORBIDDEN)
        role = get_object_or_404(JobRole, id=data.get("id"))
        serializer = JobRoleSerializer(role,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "success"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": False, "message": "Failed","error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)