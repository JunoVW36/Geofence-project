# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.core import exceptions

from rest_framework.response import Response
from rest_framework import viewsets, views
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated, AllowAny

from google.appengine.ext import ndb
try:
    from google.appengine.ext.remote_api import remote_api_stub
except ImportError:
    pass
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import urlfetch

from datalive_ndb_models.trackerPointEnt import trackerPoint
from datalive_ndb_models.trackerOutboundMessageEnt import TrackerOutboundMessage
from datalive_ndb_models.vehicleMessageEnt import VehicleMessage
from datalive_cust_veh.models import Vehicle, VehicleGroup
from datalive_auth.permissions import HasModulePermission

from . import serializers
from . import TrackerPoint
from . import TimeSheetRow
from . import TripRow
from . import StopRow
from . import TripsStops

import datetime
import calendar  #  TODO legacy, use better?

import json


MAX_POINTS_PER_DAY = 3000 # 1500 Now allow 3 days of trace at once
DATE_FORMAT_RFC_3339 = "%Y-%m-%dT%H:%M:%SZ"
#original date format= "%Y-%m-%dT%H:%M:%S.%fZ"

emptyLocation = {'place_id' : '0', 'formatted_address' : 'Unknown'}


# Can't use googlemaps library as this uses 'requests' with unsupported sockets internally
def reverseGeocode(lat, lng):
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = "latlng={latitude},{longitude}&key={apikey}".format(
        latitude=lat,
        longitude=lng,
        # TODO Need to sort this API key out properly
        apikey='AIzaSyDmbRsQfIbAGVwt2y_4T560tf3nsx2ZUyw'
    )
    url = "{base}{params}".format(base=base, params=params)

    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            locations = json.loads(result.content)
            #print locations;
            #print(locations['results'][0]['formatted_address'])
            if locations is not None:
                if len(locations) > 0:
                    return locations['results'][0]
    except urlfetch.Error:
        logging.exception('Caught exception fetching url')
    except Exception as e:
        print(e)

    print "Fail to rev-geocode!!"
    return emptyLocation #{'place_id' : '0', 'formatted_address' : 'Unknown'}


class VehicleMessageView(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        #def get(self, request, format=None):
        # Verify user has access to this vehicle
        # Verify user is loggedin
        print "post"
        print(request.data)

        # Only require this for local dev!
        # Only require this once!
        if os.environ['APPLICATION_ID'].startswith('dev'):
            local_stub = apiproxy_stub_map.apiproxy.GetStub('urlfetch')
            remote_api_stub.ConfigureRemoteApiForOAuth(
                    'datalive-staging.appspot.com',
                    '/_ah/remote_api')
            apiproxy_stub_map.apiproxy.ReplaceStub('urlfetch', local_stub)
            print "Remote NDB configured"
        else:
            pass  # we're uploaded on gae

        print "NDB config"

        try:
            vehicle_id = request.query_params['vehicle']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(vehicle_id)
        
        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            # veh_registration = vehicle.registration
            vts = vehicle.trackers.all().order_by('-installed');
            tracker_number = vts[0].tracker
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except exceptions.MultipleObjectsReturned:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Create outbound message object for listener
        tm = TrackerOutboundMessage()
        time_int = calendar.timegm(datetime.datetime.utcnow().timetuple())
        tm.key = ndb.Key('trackerOutbound', int(tracker_number), TrackerOutboundMessage, time_int) #datetime.datetime.utcnow().isoformat())
        tm.action = 3 # PEG action
        tm.state = 0 # active
        tm.userKey = None
        tm.intParameterList = [8, 1, 0] # Set output, output 1, delayed execution
        tm.stringParameterList = []
        tm.creationDateTime = datetime.datetime.utcnow()
        td = datetime.timedelta(hours=8)
        tm.timeoutDateTime = datetime.datetime.utcnow() + td
        #tm.parent = tracker_key
        tm.put()

        # create a new vehicle message entity to track message history
        #vm_key = ndb.Key(, )
        vm = VehicleMessage()
        vm.key = ndb.Key('vehicleMessageBase', int(tracker_number), VehicleMessage, datetime.datetime.utcnow().isoformat()) # parent should be based on vehicle ID not tracker ID?
        vm.vehicleKey = None # vk      old ndb links
        vm.customerKey = None # v.customerKey       old ndb links
        vm.currentTracker = int(tracker_number)
        vm.deliveredDateTime = None
        vm.acceptedDateTime = None
        vm.messageStatus = 1 # queued to send
        vm.put()

        return Response(status=status.HTTP_200_OK)


class TrackViewSet(viewsets.ViewSet):
    queryset = VehicleGroup.get_all()
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.TrackVehicleGroupSerializer
    # permission_classes = (HasModulePermission,)

    def list(self, request):
        #print(' ### user: {0} ###').format(request.user)
        #print(' &&& auth: {0} &&&').format(request.auth)

        # Only require this for local dev!
        # Only require this once!
        if os.environ['APPLICATION_ID'].startswith('dev'):
            local_stub = apiproxy_stub_map.apiproxy.GetStub('urlfetch')
            remote_api_stub.ConfigureRemoteApiForOAuth(
                    'datalive-staging.appspot.com',
                    '/_ah/remote_api')
            apiproxy_stub_map.apiproxy.ReplaceStub('urlfetch', local_stub)
            print "Remote NDB configured"
        else:
            pass  # we're uploaded on gae

        #print('NDB configured')

        groups = request.user.vehicle_groups.all().select_related('customer').prefetch_related('vehicles').defer('vehicles__trackers', 'vehicles__customer')

        # look up the latest tracker points
        for group in groups:
            print(group)
            for vehicle in group.vehicles.all():
                print(vehicle.registration)
                try:
                    vts = vehicle.trackers.all().order_by('-installed')
                    tracker_number = vts[0].tracker
                except IndexError:
                    tracker_number = 0 # no trackers attached to vehicle, so just look for a fake one

                #print(tracker_number)
                try:
                    t_key = ndb.Key('tracker', int(tracker_number))
                    points = trackerPoint.query_trackerPoint(t_key).fetch(1)
                except ValueError:
                    # 0 tracker number doesn't exist so datastore will complain about the key
                    points = []

                if len(points) > 0:
                    print(points[0])
                    vehicle.driverLabel = "No Driver ID"
                    vehicle.lat = points[0].lat / 10000000.0
                    vehicle.lon = points[0].lon / 10000000.0
                    vehicle.dateTime = points[0].updateDateTime
                    vehicle.eventCode = points[0].eventCode
                    vehicle.speed = (points[0].speed * 36.0) / 1000.0; # convert from cm/second to km/hour. !! JWF Sends as 'int' possible loss of precision !!
                    # round((vehicle.trackPoint.speed*36) / 1600);
                    vehicle.heading = points[0].heading
                    location = reverseGeocode(points[0].lat / 10000000.0,
                                                   points[0].lon / 10000000.0)
                    vehicle.locationName = location['formatted_address']
                    vehicle.locationId = location['place_id']
                    print points[0].getODO()
                    vehicle.odo = points[0].getODO() / 1000.0
                    vehicle.messageStatus = 0;
                    #try:
                    #    vehicle.odo = points[0].accum0 / 1000.0; # convert from meters to km
                    #except Exception as e:
                    #    vehicle.odo = 0;
                    #    print "tracker point has no accum0"
                    #round(points[0].accum0 / 1600) # convert from meters to miles
                else:
                    vehicle.driverLabel = "No Driver ID"
                    vehicle.lat = 0
                    vehicle.lon = 0
                    vehicle.dateTime = 0
                    vehicle.eventCode = 0
                    vehicle.speed = 0
                    vehicle.heading = 0
                    vehicle.locationName = 'None'
                    vehicle.locationId = '0'
                    vehicle.odo = 0;
                    vehicle.messageStatus = 0;

        serializer = serializers.TrackVehicleGroupSerializer(instance=groups, many=True)
        #print(repr(serializer))
        #print(serializer.data)
        return Response(serializer.data)
        """
        Return a hardcoded response.
        """
        #return Response({"success": True, "content": "Helloworld!"})



class TrackerPointViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.TrackerPointSerializer
    # permission_classes = (HasModulePermission,)

    def list(self, request):
        print(' ### user: {0} ###').format(request.user)
        print(' &&& auth: {0} &&&').format(request.auth)

        # Only require this for local dev!
        # Only require this once!
        if os.environ['APPLICATION_ID'].startswith('dev'):
            local_stub = apiproxy_stub_map.apiproxy.GetStub('urlfetch')
            remote_api_stub.ConfigureRemoteApiForOAuth(
                    'datalive-staging.appspot.com',
                    '/_ah/remote_api')
            apiproxy_stub_map.apiproxy.ReplaceStub('urlfetch', local_stub)
            print "Remote NDB configured"
        else:
            pass  # we're uploaded on gae

        # Get the vehicle ID from the query string
        try:
            vehicle_id = request.query_params['vehicle']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(vehicle_id)

        # Get dates from query string
        try:
            startdatestring = request.query_params['start']
            startdatetime = datetime.datetime.strptime(startdatestring, DATE_FORMAT_RFC_3339)
            enddatestring = request.query_params['end']
            enddatetime = datetime.datetime.strptime(enddatestring, DATE_FORMAT_RFC_3339)
            print(startdatetime)
            print(enddatetime)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            veh_registration = vehicle.registration
            vts = vehicle.trackers.all().order_by('-installed');
            tracker_number = vts[0].tracker
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except exceptions.MultipleObjectsReturned:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except IndexError:
            tracker_number = 0 # no trackers attached to vehicle, so just look for a fake one

        try:
            t_key = ndb.Key('tracker', int(tracker_number))
            #print "tracker key built"

            # Get all tracker points for this period
            points = trackerPoint.query_tracePoints(t_key, startdatetime,
                                                    enddatetime).fetch(MAX_POINTS_PER_DAY)
        except ValueError:
            # Catch bad keys for trackers that don't exist
            points = []

        # fix up points
        # Can't store the lat/lon float result as model field is an int!
        # Could stiore in a new field and only serialize that, but convert in presentaion for now.
        #for point in points:
        #    point.lat = point.lat / 10000000.0
        #    point.lon = point.lon / 10000000.0
        #    point.speed = (point.speed * 36.0) / 1000.0; # convert from cm/second to km/hour. !! JWF Sends as 'int' possible loss of precision !!

        # fix up missing accum0 from 3 wire trackers?
        # also fill in GPS ODO
        # print "fixing up accum0"
        for point in points:
            point.accum0 = point.getODO()
            #if not hasattr(point, 'accum0'):
            #    point.accum0 = 0

        serializer = serializers.TrackerPointSerializer(instance=points, many=True)
        return Response(serializer.data)

    #def retrieve(self, request, pk=None):
    #    print(' *** retrieve {0} ***\r\n').format(pk)
    #    try:
    #        trackerpoint = trackerpoints[int(pk)]
    #    except KeyError:
    #        return Response(status=status.HTTP_404_NOT_FOUND)
    #    except ValueError:
    #        return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #    serializer = serializers.TrackerPointSerializer(instance=trackerpoint)
    #    return Response(serializer.data)


class TimeSheetViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.TimeSheetRowSerializer
    # permission_classes = (HasModulePermission,)

    def processTimeSheet(cls,
                         vehicle_id, veh_registration, currentday,
                         dayStartPoint, dayStartPoint_location,
                         dayEndPoint, dayEndPoint_location,
                         drivingduration):
        # 'Locations' contain a number of results, each consisting of a 'placeid',
        #   geometry, formatted address, address type and a number of
        #   address components
        # Only the first 'location' result was stored with the point
        distance = dayEndPoint.getODO() - dayStartPoint.getODO()
        #try:
        #    distance = dayEndPoint.accum0 - dayStartPoint.accum0
        #except Exception as e:
        #    distance = 0
        #    print "tracker point has no accum0"
        timesheet = TimeSheetRow(vehicleId=vehicle_id,
                       vehicleName=veh_registration,
                       date=currentday.isoformat(),
                       driverId='0',
                       driveName='Unknown',
                       startDateTime=dayStartPoint.updateDateTime,
                       startLocationId=dayStartPoint_location['place_id'],
                       startLocationName=dayStartPoint_location['formatted_address'],
                       endDateTime=dayEndPoint.updateDateTime,
                       endLocationId=dayEndPoint_location['place_id'],
                       endLocationName=dayEndPoint_location['formatted_address'],
                       duration=dayEndPoint.updateDateTime - dayStartPoint.updateDateTime,
                       distance=distance,
                       durationDriving=drivingduration
                       )
        return timesheet


    def list(self, request):
        # debug test data
        # startdatetime = datetime.datetime(2017, 04, 10, 00, 00)
        # enddatetime = datetime.datetime(2017, 04, 16, 00, 00)
        # tracker_number = None  # 4532071844
        # veh_registration = None  # 'NotSet'

        # Only require this for local dev!
        # Only require this once!
        if os.environ['APPLICATION_ID'].startswith('dev'):
            local_stub = apiproxy_stub_map.apiproxy.GetStub('urlfetch')
            remote_api_stub.ConfigureRemoteApiForOAuth(
                    'datalive-staging.appspot.com',
                    '/_ah/remote_api')
            apiproxy_stub_map.apiproxy.ReplaceStub('urlfetch', local_stub)
            print "Remote NDB configured"
        else:
            pass  # we're uploaded on gae

        # Get the vehicle ID from the query string
        try:
            vehicle_id = request.query_params['vehicle']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(vehicle_id)

        # Get dates from query string
        try:
            startdatestring = request.query_params['start']
            startdatetime = datetime.datetime.strptime(startdatestring, DATE_FORMAT_RFC_3339)
            enddatestring = request.query_params['end']
            enddatetime = datetime.datetime.strptime(enddatestring, DATE_FORMAT_RFC_3339)
            print(startdatetime)
            print(enddatetime)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            veh_registration = vehicle.registration
            vts = vehicle.trackers.all().order_by('-installed');
            tracker_number = vts[0].tracker
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except exceptions.MultipleObjectsReturned:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        t_key = ndb.Key('tracker', int(tracker_number))
        print "timesheet tracker key built"

        timesheets = []

        # Should pull out user configured timezone and working week?

        # Split time period into working days
        # Should consider users / vehicle timezone
        currentdaystart = startdatetime.replace(hour=0, minute=0, second=0, microsecond=0)
        #endday = enddatetime.date()
        dayperiod = datetime.timedelta(hours=24)

        while currentdaystart < enddatetime:
            # Get all tracker points for this day
            points = trackerPoint.query_tracePoints(t_key, currentdaystart,
                                                    currentdaystart + dayperiod).fetch(MAX_POINTS_PER_DAY)
            print "Retrived points for %s" % (currentdaystart.isoformat())

            # Process timesheet day
            # We consider first key on as start of day - may be other IO inputs that some users would like considering?
            # If the first point in the day is some sort of driving point then consider start of activity to be midnight?
            # Last key off as end of day
            daystartpoint = None
            dayendpoint = None
            daydrivestart = None
            daydrivingduration = datetime.timedelta()
            for point in points:
                # debug print event code
                #print "%s: ec %d" % (point.updateDateTime, point.eventCode)

                # look for 1st key on
                if (daystartpoint is None) and (point.eventCode == 4):
                    daystartpoint = point

                # mark possible final key off
                if (daystartpoint is not None) and (point.eventCode == 5):
                    dayendpoint = point

                # find individual trip fragments and sum driving time
                if point.eventCode == 4:
                    daydrivestart = point
                if (daydrivestart is not None) and (point.eventCode == 5):
                    daydrivingduration = daydrivingduration + (point.updateDateTime - daydrivestart.updateDateTime)
                    daydrivestart = None

            if (daystartpoint is not None) and (dayendpoint is not None):
                print "start %s" % (daystartpoint.updateDateTime.isoformat())
                print "end %s" % (dayendpoint.updateDateTime.isoformat())
                daystart_location = reverseGeocode(daystartpoint.lat / 10000000.0,
                                                   daystartpoint.lon / 10000000.0)
                dayend_location = reverseGeocode(dayendpoint.lat / 10000000.0,
                                                   dayendpoint.lon / 10000000.0)
                timesheet = self.processTimeSheet(vehicle_id, veh_registration,
                                                  currentdaystart.date(),
                                                  daystartpoint, daystart_location,
                                                  dayendpoint, dayend_location,
                                                  daydrivingduration)
                timesheets.append(timesheet)
            else:
                timesheet = TimeSheetRow(vehicleId=vehicle_id,
                       vehicleName=veh_registration,
                       date=currentdaystart.date().isoformat(),
                       driverId='0',
                       driveName='Unknown',
                       startDateTime=currentdaystart,
                       startLocationId=0,
                       startLocationName='None',
                       endDateTime=currentdaystart,
                       endLocationId=0,
                       endLocationName='None',
                       duration=datetime.timedelta(),
                       distance=0,
                       durationDriving=datetime.timedelta()
                       )
                timesheets.append(timesheet)
                print "no activity for this day"

            currentdaystart = currentdaystart + dayperiod

        serializer = serializers.TimeSheetRowSerializer(instance=timesheets, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, pk=None): would retrieve a set of trip rows?


class TripViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.TripRowSerializer

    def processTrip(cls, vehicle_id, veh_registration, tripCount,
                    tripStartPoint, tripStartPoint_location,
                    tripEndPoint, tripEndPoint_location):
        # 'Locations' contain a number of results, each consisting of a 'placeid',
        #   geometry, formatted address, address type and a number of
        #   address components
        # Only the first 'location' result was stored with the point
        distance = tripEndPoint.getODO() - tripStartPoint.getODO()
        #try:
        #    distance = tripEndPoint.accum0 - tripStartPoint.accum0
        #except Exception as e:
        #    distance = 0
        #    print "tracker point has no accum0"
        trip = TripRow(#vehicleId=vehicle_id,
                       #vehicleName=veh_registration,
                       date=tripStartPoint.updateDateTime.date().isoformat(),
                       tripNumber=tripCount, tripId='Not Set',
                       driverId='0',
                       driveName='Unknown',
                       startDateTime=tripStartPoint.updateDateTime,
                       startLocationId=tripStartPoint_location['place_id'],
                       startLocationName=tripStartPoint_location['formatted_address'],
                       endDateTime=tripEndPoint.updateDateTime,
                       endLocationId=tripEndPoint_location['place_id'],
                       endLocationName=tripEndPoint_location['formatted_address'],
                       duration=tripEndPoint.updateDateTime - tripStartPoint.updateDateTime,
                       distance=distance
                       )
        return trip

    def processStop(cls, stopCount, arrivalPoint, arrivalPoint_location,
                    departurePoint):
        stop = StopRow(date=arrivalPoint.updateDateTime.date().isoformat(),
                       stopNumber=stopCount, stopId='Not Set',
                       arrivalDateTime=arrivalPoint.updateDateTime,
                       arrivalLocationId=arrivalPoint_location['place_id'],
                       arrivalLocationName=arrivalPoint_location['formatted_address'],
                       duration=departurePoint.updateDateTime - arrivalPoint.updateDateTime
                       )
        return stop

    def list(self, request):
        # debug test data
        # startdatetime = datetime.datetime(2017, 04, 10, 00, 00)
        # enddatetime = datetime.datetime(2017, 04, 16, 00, 00)
        # tracker_number = None  # 4532071844
        # veh_registration = None  # 'NotSet'

        # Only require this for local dev!
        # Only require this once!
        if os.environ['APPLICATION_ID'].startswith('dev'):
            local_stub = apiproxy_stub_map.apiproxy.GetStub('urlfetch')
            remote_api_stub.ConfigureRemoteApiForOAuth(
                    'datalive-staging.appspot.com',
                    '/_ah/remote_api')
            apiproxy_stub_map.apiproxy.ReplaceStub('urlfetch', local_stub)
            print "Remote NDB configured"
        else:
            pass  # we're uploaded on gae

        # Get the vehicle ID from the query string
        try:
            vehicle_id = request.query_params['vehicle']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(vehicle_id)

        # Get dates from query string
        try:
            startdatestring = request.query_params['start']
            startdatetime = datetime.datetime.strptime(startdatestring, DATE_FORMAT_RFC_3339)
            enddatestring = request.query_params['end']
            enddatetime = datetime.datetime.strptime(enddatestring, DATE_FORMAT_RFC_3339)
            print(startdatetime)
            print(enddatetime)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            veh_registration = vehicle.registration
            vts = vehicle.trackers.all().order_by('-installed');
            tracker_number = vts[0].tracker
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except exceptions.MultipleObjectsReturned:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        t_key = ndb.Key('tracker', int(tracker_number))
        print "tracker key built"

        # Set up 'trip' vars
        tripCount = 0  # no trips
        trips = []
        tripStartPoint = None  # trip not yet started
        tripPossibleEndPoint = None

        # Set up 'stops' vars
        stopCount = 0
        stops = []

        # Get all tracker points for this period
        points = trackerPoint.query_tracePoints(t_key, startdatetime,
                                                enddatetime).fetch(MAX_POINTS_PER_DAY)
        print "Retrived points"

        for point in points:
            # debug print event code
            # print "%s: ec %d" % (point.updateDateTime, point.eventCode)

            # 'Key Off' and no trip started
            if (point.eventCode == 5) and (tripStartPoint is None):
                print "Started on a partial trip"

            # 'Key On' and no start of trip yet recorded
            # This will only happen on the 1st trip we find, all others the start
            # point is found as part of the trip end discovery process.
            if (point.eventCode == 4) and (tripStartPoint is None):
                tripStartPoint = point
                tripStartPoint_location = reverseGeocode(tripStartPoint.lat / 10000000.0,
                                                              tripStartPoint.lon / 10000000.0)

            # 'Key Off' and trip has started
            if (point.eventCode == 5) and (tripStartPoint is not None):
                tripPossibleEndPoint = point

            # 'Key On' and trip possible end found
            if (point.eventCode == 4) and (tripPossibleEndPoint is not None):
                if ((point.updateDateTime - tripPossibleEndPoint.updateDateTime) < datetime.timedelta(seconds=30)):
                    # short stop, possible start stop ign, ignore
                    tripPossibleEndPoint = None
                else:
                    # We've found the start of a genuine new trip, so we can
                    # close off the old trip we had.
                    # We've found a real trip (previous possible end point)
                    # Create a new point that is the average of the possible end
                    # and new start locations, then just do one reverse geocode
                    # look up for only this point.
                    # TODO Could make better choices here based on sat count and HDOP
                    tripPossibleEndPoint.lat = (tripPossibleEndPoint.lat + point.lat) / 2
                    tripPossibleEndPoint.lon = (tripPossibleEndPoint.lon + point.lon) / 2
                    tripPossibleEndPoint_location = reverseGeocode(tripPossibleEndPoint.lat / 10000000.0,
                                                                         tripPossibleEndPoint.lon / 10000000.0)
                    trip = self.processTrip(vehicle_id, veh_registration, tripCount,
                                       tripStartPoint, tripStartPoint_location,
                                       tripPossibleEndPoint, tripPossibleEndPoint_location)

                    # add trip to list
                    tripCount += 1
                    trips.append(trip)

                    stop = self.processStop(stopCount, tripPossibleEndPoint,
                                            tripPossibleEndPoint_location,
                                            point)

                    # add stop to list
                    stopCount += 1
                    stops.append(stop)

                    # Mark start of new trip, use the averaged location data we've already looked up
                    tripStartPoint = point
                    tripStartPoint.lat = tripPossibleEndPoint.lat
                    tripStartPoint.lon = tripPossibleEndPoint.lon
                    tripStartPoint_location = tripPossibleEndPoint_location
                    tripPossibleEndPoint = None

        if tripPossibleEndPoint is not None:
            # process the final trip that had no following key on to help identify it
            tripPossibleEndPoint_location = reverseGeocode(tripPossibleEndPoint.lat / 10000000.0,
                                                                tripPossibleEndPoint.lon / 10000000.0)
            trip = self.processTrip(vehicle_id, veh_registration, tripCount,
                               tripStartPoint, tripStartPoint_location,
                               tripPossibleEndPoint, tripPossibleEndPoint_location)
            # add trip to list
            tripCount += 1
            trips.append(trip)

        print "Processed trips"

        tripsStops = TripsStops(vehicleId=vehicle_id, vehicleName=veh_registration)
        tripsStops.trips = trips
        tripsStops.stops = stops
        serializer = serializers.TripsStopsSerializer(instance=tripsStops) #TripRowSerializer(instance=trips, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, pk=None): would retrieve a set of journey rows?


class IndexView(TemplateView):
    template_name = 'index.html'

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)



