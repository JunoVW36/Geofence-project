from rest_framework import serializers
from .models import *
from datalive_cust_veh.models import *



class VehicleGroupContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleGroupContact
        fields = '__all__'

