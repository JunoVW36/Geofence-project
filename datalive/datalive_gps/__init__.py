class VehicleMessage(object):
    def __init__(self, **kwargs):
        for field in ('vehicleId', 'message', 'notificationType'
                      ):
            setattr(self, field, kwargs.get(field, None))


# Sample for test purposes
class TrackerPoint(object):
    def __init__(self, **kwargs):
        for field in ('id', 'lat', 'lon', 'updateDateTime', 'heading',
                      'speed', 'eventCode'):
            setattr(self, field, kwargs.get(field, None))


class TimeSheetRow(object):
    def __init__(self, **kwargs):
        for field in ('vehicleId', 'vehicleName',  # move out to containing json
                      'date',
                      'driverId', 'driveName',
                      'startDateTime', 'startLocationId', 'startLocationName',
                      'endDateTime', 'endLocationId', 'endLocationName',
                      'duration', 'distance', 'durationDriving'
                      ):
            setattr(self, field, kwargs.get(field, None))


class TripRow(object):
    def __init__(self, **kwargs):
        for field in ('date',
                      'tripNumber', 'tripId',
                      'driverId', 'driveName',
                      'startDateTime', 'startLocationId', 'startLocationName',
                      'endDateTime', 'endLocationId', 'endLocationName',
                      'duration', 'distance',
                      ):
            setattr(self, field, kwargs.get(field, None))


class StopRow(object):
    def __init__(self, **kwargs):
        for field in ('date',
                      'stopNumber', 'stopId',
                      'arrivalDateTime', 'arrivalLocationId', 'arrivalLocationName',
                      'duration',
                      ):
            setattr(self, field, kwargs.get(field, None))


class TripsStops(object):
    def __init__(self, **kwargs):
        for field in ('vehicleId', 'vehicleName',):
            setattr(self, field, kwargs.get(field, None))


class TrackRow(object):
    def __init__(self, **kwargs):
        for field in ('vehicleId', 'vehicleName',
                      'driverId', 'driveName',
                      'lat', 'lon', 'locationName', 'locationId',
                      'dateTime', 'eventCode', 'speed', 'heading',
                      'odo'
                      ):
            setattr(self, field, kwargs.get(field, None))

