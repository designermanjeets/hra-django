from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Permission
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'gender', 'job_role', 'tenant_id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        default_password = 'password'
        password = validated_data.get('password', default_password)
        
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            gender=validated_data['gender'],
            job_role=validated_data['job_role'],
            tenant_id=validated_data['tenant_id']
        )
        user.set_password(password)
        user.save()
        return user
    

class EmpDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpDetail
        fields = '__all__'

class AddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressDetail
        fields = '__all__'

class PersonalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetail
        fields = '__all__'

class VisadetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visadetail
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'