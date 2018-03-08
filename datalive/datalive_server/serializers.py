from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import Defect, EquipmentFault, Equipment, DefectSetting

''' 
A separate serializer for the server auth endpoint if we need it
'''

class XlrDefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defect
        fields = '__all__'


