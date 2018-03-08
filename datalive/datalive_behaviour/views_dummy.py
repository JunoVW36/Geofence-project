# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView

from google.appengine.ext import ndb
try:
    from google.appengine.ext.remote_api import remote_api_stub
except ImportError:
    pass
from google.appengine.api import apiproxy_stub_map

from datalive_gps.datalive_ndb_models.trackerPointEnt import trackerPoint
from datalive_cust_veh.models import Vehicle, VehicleGroup
from datalive_auth.permissions import HasModulePermission

from . import serializers
from . import BehaviourSafetyABCVehicleRow
from . import BehaviourSafetyABCVehicle
from . import BehaviourSafetyMobileEyeVehicleRow
from . import BehaviourSafetyMobileEyeVehicle

import datetime

import json



MAX_POINTS_PER_DAY = 3000 # 1500 Now allow 3 days of trace at once
DATE_FORMAT_RFC_3339 = "%Y-%m-%dT%H:%M:%SZ"


class SafetyABCVehicleViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.BehaviourSafetyABCVehicleSerializer

    def list(self, request):
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

        # Get the vehicle Group ID from the query string
        try:
            vehicle_group_id = request.query_params['vehicle_group']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(vehicle_group_id)

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
            vehicle_group = VehicleGroup.objects.get(pk=vehicle_group_id)
            #veh_registration = vehicle.registration
            #vts = vehicle.trackers.all().order_by('-installed');
            #tracker_number = vts[0].tracker
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except exceptions.MultipleObjectsReturned:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(vehicle_group)

        safety_rows = []

        for vehicle in vehicle_group.vehicles.all():
            print(vehicle.registration)
            vts = vehicle.trackers.all().order_by('-installed')
            tracker_number = vts[0].tracker
            print(tracker_number)
            t_key = ndb.Key('tracker', int(tracker_number))
            #points = trackerPoint.query_trackerPoint(t_key).fetch(1)
            print(safety_rows)
            safety_rows.append(BehaviourSafetyABCVehicleRow(vehicleId=vehicle.id,
                                                            vehicleName=vehicle.registration,
                                                            score=86.3,
                                                            distance=459.3,
                                                            duration=datetime.timedelta(),
                                                            aPerThousand=12,
                                                            aCount=6,
                                                            bPerThousand=12,
                                                            bCount=6,
                                                            cPerThousand=12,
                                                            cCount=6,
                                                            speedingDistance=120,
                                                            idleDuration=datetime.timedelta(),
                                                        ))
        safety_rows.append(BehaviourSafetyABCVehicleRow(vehicleId=vehicle.id,
                                                                    vehicleName=vehicle.registration,
                                                                    score=74.3,
                                                                    distance=387.3,
                                                                    duration=datetime.timedelta(),
                                                                    aPerThousand=15,
                                                                    aCount=8,
                                                                    bPerThousand=12,
                                                                    bCount=6,
                                                                    cPerThousand=16,
                                                                    cCount=7,
                                                                    speedingDistance=150,
                                                                    idleDuration=datetime.timedelta(),
                                                            ))
        safety_rows.append(BehaviourSafetyABCVehicleRow(vehicleId=vehicle.id,
                                                                    vehicleName=vehicle.registration,
                                                                    score=74.3,
                                                                    distance=387.3,
                                                                    duration=datetime.timedelta(),
                                                                    aPerThousand=15,
                                                                    aCount=8,
                                                                    bPerThousand=12,
                                                                    bCount=6,
                                                                    cPerThousand=16,
                                                                    cCount=7,
                                                                    speedingDistance=150,
                                                                    idleDuration=datetime.timedelta(),
                                                            ))
        safety_rows.append(BehaviourSafetyABCVehicleRow(vehicleId=vehicle.id,
                                                                    vehicleName=vehicle.registration,
                                                                    score=73.1,
                                                                    distance=329.2,
                                                                    duration=datetime.timedelta(),
                                                                    aPerThousand=18,
                                                                    aCount=7,
                                                                    bPerThousand=19,
                                                                    bCount=9,
                                                                    cPerThousand=16,
                                                                    cCount=4,
                                                                    speedingDistance=150,
                                                                    idleDuration=datetime.timedelta(),
                                                            ))
        safety_rows.append(BehaviourSafetyABCVehicleRow(vehicleId=vehicle.id,
                                                                    vehicleName=vehicle.registration,
                                                                    score=72.1,
                                                                    distance=319.2,
                                                                    duration=datetime.timedelta(),
                                                                    aPerThousand=13,
                                                                    aCount=6,
                                                                    bPerThousand=21,
                                                                    bCount=9,
                                                                    cPerThousand=14,
                                                                    cCount=4,
                                                                    speedingDistance=110,
                                                                    idleDuration=datetime.timedelta(),
                                                            ))
        safety_rows.append(BehaviourSafetyABCVehicleRow(vehicleId=vehicle.id,
                                                                    vehicleName=vehicle.registration,
                                                                    score=68.1,
                                                                    distance=319.2,
                                                                    duration=datetime.timedelta(),
                                                                    aPerThousand=19,
                                                                    aCount=12,
                                                                    bPerThousand=21,
                                                                    bCount=9,
                                                                    cPerThousand=14,
                                                                    cCount=4,
                                                                    speedingDistance=180,
                                                                    idleDuration=datetime.timedelta(),
                                                            ))
            

        safety = BehaviourSafetyABCVehicle(vehicleGroupId=vehicle_group_id, 
                                           vehicleGroupName=vehicle_group.name,
                                           startDateTime=startdatetime,
                                           endDateTime=enddatetime,
                                           weightA=20.0,
                                           weightB=20.0,
                                           weightC=20.0,
                                           weightS=20.0,
                                           weightI=20.0,
                                           averageScore=50.0,
                                           totalDistance=23564.7,
                                           averageAPerThousand=12.6,
                                           totalACount=197,
                                           averageBPerThousand=2.7,
                                           totalBCount=56,
                                           averageCPerThousand=56.4,
                                           totalCCount=56,
                                           totalSpeedingDistance=4503.7,
                                           totalIdleDuration=datetime.timedelta(),
                                           )
        safety.rows = safety_rows
        serializer = serializers.BehaviourSafetyABCVehicleSerializer(instance=safety)
        return Response(serializer.data)


class SafetyMobileEyeVehicleViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = serializers.BehaviourSafetyMobileEyeVehicleSerializer

    def list(self, request):
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

        # Get the vehicle Group ID from the query string
        try:
            vehicle_group_id = request.query_params['vehicle_group']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(vehicle_group_id)

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
            vehicle_group = VehicleGroup.objects.get(pk=vehicle_group_id)
            #veh_registration = vehicle.registration
            #vts = vehicle.trackers.all().order_by('-installed');
            #tracker_number = vts[0].tracker
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except exceptions.MultipleObjectsReturned:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(vehicle_group)

        safety_rows = []

        for vehicle in vehicle_group.vehicles.all():
            print(vehicle.registration)
            vts = vehicle.trackers.all().order_by('-installed')
            tracker_number = vts[0].tracker
            print(tracker_number)
            t_key = ndb.Key('tracker', int(tracker_number))
            #points = trackerPoint.query_trackerPoint(t_key).fetch(1)

            safety_rows.append(BehaviourSafetyMobileEyeVehicleRow(vehicleId=vehicle.id,
                                                                  vehicleName=vehicle.registration,
                                                                  score=86.3,
                                                                  distance=459.3,
                                                                  ldwPerThousand=12,
                                                                  ldwCount=6,
                                                                  hwPerThousand=12,
                                                                  hwCount=6,
                                                                  ucwPerThousand=12,
                                                                  ucwCount=6,
                                                                  fcwPerThousand=12,
                                                                  fcwCount=6,
                                                                  pdzPerThousand=12,
                                                                  pdzCount=6,
                                                                  sPerThousand=10,
                                                                  sCount=10,
                                                                  ))
        safety_rows.append(BehaviourSafetyMobileEyeVehicleRow(vehicleId=vehicle.id,
                                                                  vehicleName=vehicle.registration,
                                                                  score=83.3,
                                                                  distance=225.3112,
                                                                  ldwPerThousand=13,
                                                                  ldwCount=6,
                                                                  hwPerThousand=16.22,
                                                                  hwCount=6,
                                                                  ucwPerThousand=16,
                                                                  ucwCount=6,
                                                                  fcwPerThousand=13,
                                                                  fcwCount=6,
                                                                  pdzPerThousand=19.333,
                                                                  pdzCount=12,
                                                                  sPerThousand=10,
                                                                  sCount=10,
                                                                  ))
        safety_rows.append(BehaviourSafetyMobileEyeVehicleRow(vehicleId=vehicle.id,
                                                                  vehicleName=vehicle.registration,
                                                                  score=70.3,
                                                                  distance=459.3,
                                                                  ldwPerThousand=16,
                                                                  ldwCount=8,
                                                                  hwPerThousand=19,
                                                                  hwCount=6,
                                                                  ucwPerThousand=21,
                                                                  ucwCount=9,
                                                                  fcwPerThousand=12,
                                                                  fcwCount=6,
                                                                  pdzPerThousand=20,
                                                                  pdzCount=6,
                                                                  sPerThousand=10,
                                                                  sCount=10,
                                                                  ))

        safety = BehaviourSafetyMobileEyeVehicle(vehicleGroupId=vehicle_group_id, 
                                                 vehicleGroupName=vehicle_group.name,
                                                 startDateTime=startdatetime,
                                                 endDateTime=enddatetime,
                                                 weightLDW=17.0,
                                                 weightHW=16.0,
                                                 weightUCW=16.0,
                                                 weightFCW=16.0,
                                                 weightPDZ=16.0,
                                                 weightS=16.0,
                                                 averageScore=45.8,
                                                 totalDistance=234567.6,
                                                 averageLDWPerThousand=34.6,
                                                 totalLDWCount=57,
                                                 averageHWPerThousand=45.34433,
                                                 totalHWCount=89,
                                                 averageUCWPerThousand=34.833,
                                                 totalUCWCount=90,
                                                 averageFCWPerThousand=23.4,
                                                 totalFCWCount=234,
                                                 averagePDZPerThousand=89.5,
                                                 totalPDZCount=56,
                                                 averageSPerThousand=56.2,
                                                 totalSCount=9898,
                                                 )
        safety.rows = safety_rows
        serializer = serializers.BehaviourSafetyMobileEyeVehicleSerializer(instance=safety)
        return Response(serializer.data)




