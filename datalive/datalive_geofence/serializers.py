from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import Geofence, GeofenceBoundingBox, GeofenceBoundingBox, GeofenceGroup, GeofenceCategory


class GeofenceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GeofenceCategory
        fields = '__all__'

class GeofenceGroupSerializer(serializers.ModelSerializer):
    category = GeofenceCategorySerializer(many=True)

    class Meta:
        model = GeofenceGroup
        fields = '__all__'


class GeofenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geofence
        fields = '__all__'
