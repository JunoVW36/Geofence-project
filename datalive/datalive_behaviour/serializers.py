from rest_framework import serializers


class BehaviourSafetyABCVehicleRowSerializer(serializers.Serializer):
    vehicleId = serializers.CharField(read_only=True)
    vehicleName = serializers.CharField(read_only=True)
    score = serializers.FloatField(read_only=True)
    distance = serializers.FloatField(read_only=True)
    duration = serializers.DurationField(read_only=True)
    aPerThousand = serializers.FloatField(read_only=True)
    aCount = serializers.IntegerField(read_only=True)
    bPerThousand = serializers.FloatField(read_only=True)
    bCount = serializers.IntegerField(read_only=True)
    cPerThousand = serializers.FloatField(read_only=True)
    cCount = serializers.IntegerField(read_only=True)
    speedingDistance = serializers.FloatField(read_only=True)
    idleDuration = serializers.DurationField(read_only=True)


class BehaviourSafetyABCVehicleSerializer(serializers.Serializer):
    vehicleGroupId = serializers.CharField(read_only=True)
    vehicleGroupName = serializers.CharField(read_only=True)
    startDateTime = serializers.DateTimeField(read_only=True)
    endDateTime = serializers.DateTimeField(read_only=True)
    weightA = serializers.FloatField(read_only=True)  # Acceleration
    weightB = serializers.FloatField(read_only=True)  # Braking
    weightC = serializers.FloatField(read_only=True)  # Cornering
    weightS = serializers.FloatField(read_only=True)  # Speeding
    weightI = serializers.FloatField(read_only=True)  # Idling
    averageScore = serializers.FloatField(read_only=True)
    totalDistance = serializers.FloatField(read_only=True)
    averageAPerThousand = serializers.FloatField(read_only=True)
    totalACount = serializers.IntegerField(read_only=True)
    averageBPerThousand = serializers.FloatField(read_only=True)
    totalBCount = serializers.IntegerField(read_only=True)
    averageCPerThousand = serializers.FloatField(read_only=True)
    totalCCount = serializers.IntegerField(read_only=True)
    totalSpeedingDistance = serializers.FloatField(read_only=True)
    totalIdleDuration = serializers.DurationField(read_only=True)
    rows = BehaviourSafetyABCVehicleRowSerializer(many=True)


class BehaviourSafetyMobileEyeVehicleRowSerializer(serializers.Serializer):
    vehicleId = serializers.CharField(read_only=True)
    vehicleName = serializers.CharField(read_only=True)
    score = serializers.FloatField(read_only=True)
    distance = serializers.FloatField(read_only=True)
    ldwPerThousand = serializers.FloatField(read_only=True)
    ldwCount = serializers.IntegerField(read_only=True)
    hwPerThousand = serializers.FloatField(read_only=True)
    hwCount = serializers.IntegerField(read_only=True)
    ucwPerThousand = serializers.FloatField(read_only=True)
    ucwCount = serializers.IntegerField(read_only=True)
    fcwPerThousand = serializers.FloatField(read_only=True)
    fcwCount = serializers.IntegerField(read_only=True)
    pdzPerThousand = serializers.FloatField(read_only=True)
    pdzCount = serializers.IntegerField(read_only=True)
    sPerThousand = serializers.FloatField(read_only=True)
    sCount = serializers.IntegerField(read_only=True)


class BehaviourSafetyMobileEyeVehicleSerializer(serializers.Serializer):
    vehicleGroupId = serializers.CharField(read_only=True)
    vehicleGroupName = serializers.CharField(read_only=True)
    startDateTime = serializers.DateTimeField(read_only=True)
    endDateTime = serializers.DateTimeField(read_only=True)
    weightLDW = serializers.FloatField(read_only=True)  # Acceleration
    weightHW = serializers.FloatField(read_only=True)  # Braking
    weightUCW = serializers.FloatField(read_only=True)  # Cornering
    weightFCW = serializers.FloatField(read_only=True)  # Speeding
    weightPDZ = serializers.FloatField(read_only=True)  # Idling
    weightS = serializers.FloatField(read_only=True)  # Speeding
    averageScore = serializers.FloatField(read_only=True)
    totalDistance = serializers.FloatField(read_only=True)
    averageLDWPerThousand = serializers.FloatField(read_only=True)
    totalLDWCount = serializers.IntegerField(read_only=True)
    averageHWPerThousand = serializers.FloatField(read_only=True)
    totalHWCount = serializers.IntegerField(read_only=True)
    averageUCWPerThousand = serializers.FloatField(read_only=True)
    totalUCWCount = serializers.IntegerField(read_only=True)
    averageFCWPerThousand = serializers.FloatField(read_only=True)
    totalFCWCount = serializers.IntegerField(read_only=True)
    averagePDZPerThousand = serializers.FloatField(read_only=True)
    totalPDZCount = serializers.IntegerField(read_only=True)
    averageSPerThousand = serializers.FloatField(read_only=True)
    totalSCount = serializers.IntegerField(read_only=True)
    rows = BehaviourSafetyMobileEyeVehicleRowSerializer(many=True)

