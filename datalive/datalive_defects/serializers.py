from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import Defect, EquipmentDefinition, EquipmentDefinitionFault, EquipmentResponse


class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defect
        fields = '__all__'


class FaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentDefinitionFault
        fields = ['id', 'fault', 'description']
        

class EquipmentSerializer(serializers.ModelSerializer):
    faults = FaultSerializer(required=False, many=True)
    class Meta:
        model = EquipmentDefinition
        fields = ['id', 'equipment_name', 'faults', 'customer']


class EquipmentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentResponse
        fields = '__all__' 
        
    
    


