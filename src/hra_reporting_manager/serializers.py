from rest_framework import serializers
from .models import ReportingManager

class ReportingManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportingManager
        fields = '__all__'