class BehaviourSafetyABCVehicleRow(object):
    def __init__(self, **kwargs):
        for field in ('vehicleId', 'vehicleName', 'score',
                      'distance', 'duration',
                      'aPerThousand', 'aCount',
                      'bPerThousand', 'bCount',
                      'cPerThousand', 'cCount',
                      'speedingDistance', 'idleDuration',
                      ):
            setattr(self, field, kwargs.get(field, None))


class BehaviourSafetyABCVehicle(object):
    def __init__(self, **kwargs):
        for field in ('vehicleGroupId', 'vehicleGroupName',
                      'startDateTime', 'endDateTime', 
                      'weightA', 'weightB', 'weightC', 'weightS', 'weightI',
                      'averageScore', 'totalDistance',
                      'averageAPerThousand', 'totalACount',
                      'averageBPerThousand', 'totalBCount',
                      'averageCPerThousand', 'totalCCount',
                      'totalSpeedingDistance', 'totalIdleDuration',
                      ):
            setattr(self, field, kwargs.get(field, None))


class BehaviourSafetyMobileEyeVehicleRow(object):
    def __init__(self, **kwargs):
        for field in ('vehicleId', 'vehicleName', 'score',
                      'distance',
                      'ldwPerThousand', 'ldwCount',
                      'hwPerThousand', 'hwCount',
                      'ucwPerThousand', 'ucwCount',
                      'fcwPerThousand', 'fcwCount',
                      'pdzPerThousand', 'pdzCount',
                      'sPerThousand', 'sCount',
                      ):
            setattr(self, field, kwargs.get(field, None))


class BehaviourSafetyMobileEyeVehicle(object):
    def __init__(self, **kwargs):
        for field in ('vehicleGroupId', 'vehicleGroupName',
                      'startDateTime', 'endDateTime', 
                      'weightLDW', 'weightHW', 'weightUCW', 'weightFCW', 'weightPDZ', 'weightS',
                      'averageScore', 'totalDistance',
                      'averageLDWPerThousand', 'totalLDWCount',
                      'averageHWPerThousand', 'totalHWCount',
                      'averageUCWPerThousand', 'totalUCWCount',
                      'averageFCWPerThousand', 'totalFCWCount',
                      'averagePDZPerThousand', 'totalPDZCount',
                      'averageSPerThousand', 'totalSCount',
                      ):
            setattr(self, field, kwargs.get(field, None))


