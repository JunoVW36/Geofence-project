from rest_framework import serializers
from . import TrackerPoint
from datalive_cust_veh.models import VehicleGroup, VehicleTracker, Vehicle


class VehicleMessageSerializer(serializers.Serializer):
    vehicleId = serializers.CharField()
    notificationType = serializers.IntegerField()
    message = serializers.CharField()


class TimeSheetRowSerializer(serializers.Serializer):
    vehicleId = serializers.CharField(read_only=True)  # move out to containing
    vehicleName = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    driverId = serializers.CharField(read_only=True)
    driveName = serializers.CharField(read_only=True)
    startDateTime = serializers.DateTimeField(read_only=True)
    startLocationId = serializers.CharField(read_only=True)
    startLocationName = serializers.CharField(read_only=True)
    endDateTime = serializers.DateTimeField(read_only=True)
    endLocationId = serializers.CharField(read_only=True)
    endLocationName = serializers.CharField(read_only=True)
    duration = serializers.DurationField(read_only=True)
    distance = serializers.FloatField(read_only=True)
    durationDriving = serializers.DurationField(read_only=True)


class TripRowSerializer(serializers.Serializer):
    #vehicleId = serializers.CharField(read_only=True)  # move out to containing
    #vehicleName = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    tripNumber = serializers.IntegerField(read_only=True)
    tripId = serializers.CharField(read_only=True)
    driverId = serializers.CharField(read_only=True)
    driveName = serializers.CharField(read_only=True)
    startDateTime = serializers.DateTimeField(read_only=True)
    startLocationId = serializers.CharField(read_only=True)
    startLocationName = serializers.CharField(read_only=True)
    endDateTime = serializers.DateTimeField(read_only=True)
    endLocationId = serializers.CharField(read_only=True)
    endLocationName = serializers.CharField(read_only=True)
    duration = serializers.DurationField(read_only=True)
    distance = serializers.FloatField(read_only=True)


class StopRowSerializer(serializers.Serializer):
    date = serializers.DateTimeField(read_only=True)
    stopNumber = serializers.IntegerField(read_only=True)
    stopId = serializers.CharField(read_only=True)
    arrivalDateTime = serializers.DateTimeField(read_only=True)
    arrivalLocationId = serializers.CharField(read_only=True)
    arrivalLocationName = serializers.CharField(read_only=True)
    duration = serializers.DurationField(read_only=True)


class TripsStopsSerializer(serializers.Serializer):
    vehicleId = serializers.CharField(read_only=True)
    vehicleName = serializers.CharField(read_only=True)
    trips = TripRowSerializer(many=True)
    stops = StopRowSerializer(many=True)


class TrackVehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    registration = serializers.CharField(read_only=True)
    fleet_id = serializers.CharField(read_only=True)
    vin = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    archived = serializers.BooleanField(read_only=True)
    driverLabel = serializers.CharField(read_only=True)
    lat = serializers.FloatField(read_only=True)
    lon = serializers.FloatField(read_only=True)
    locationName = serializers.CharField(read_only=True)
    locationId = serializers.CharField(read_only=True)
    dateTime = serializers.DateTimeField(read_only=True)
    eventCode = serializers.IntegerField(read_only=True)
    speed = serializers.IntegerField(read_only=True)
    heading = serializers.IntegerField(read_only=True)
    odo = serializers.IntegerField(read_only=True)
    messageStatus = serializers.IntegerField(read_only=True)


#    vehicleId = serializers.CharField(read_only=True)
#    vehicleName = serializers.CharField(read_only=True)
#    driverId = serializers.CharField(read_only=True)
#    driveName = serializers.CharField(read_only=True)
#    lat = serializers.FloatField(read_only=True)
#    lon = serializers.FloatField(read_only=True)
#    locationName = serializers.CharField(read_only=True)
#    locationId = serializers.CharField(read_only=True)
#    dateTime = serializers.DateTimeField(read_only=True)
#    eventCode = serializers.IntegerField(read_only=True)
#    speed = serializers.IntegerField(read_only=True)
#    heading = serializers.IntegerField(read_only=True)
#    odo = serializers.FloatField(read_only=True)


class TrackVehicleGroupSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    vehicles = TrackVehicleSerializer(many=True)


class TrackerPointSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    updateDateTime = serializers.DateTimeField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    heading = serializers.IntegerField()
    speed = serializers.IntegerField()
    eventCode = serializers.IntegerField()
    accum0 = serializers.IntegerField() # may not exist


