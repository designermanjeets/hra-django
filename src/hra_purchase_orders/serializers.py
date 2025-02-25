from rest_framework import serializers
from .models import *

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        

class AssignPurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignPurchaseOrder
        fields = '__all__'
        