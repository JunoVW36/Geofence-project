# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.shortcuts import render
from django.core import exceptions

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


MAX_POINTS_PER_DAY = 3000 # Allow for all keyon/off during a week
DATE_FORMAT_RFC_3339 = "%Y-%m-%dT%H:%M:%SZ"



def calcScoreComponent(metric, baseline_low, baseline_high, weight):
    score = 0
    if metric < baseline_high:
        score = (baseline_high - metric) / (baseline_high - baseline_low) * weight
        if score > weight:
            score = weight
    return score


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
        except VehicleGroup.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except exceptions.MultipleObjectsReturned:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # In future pull these weights from a config
        weight_a = 20.0
        weight_b = 20.0
        weight_c = 20.0
        weight_s = 20.0
        weight_i = 20.0
        a_score_baseline_low = 2.0
        b_score_baseline_low = 1.0
        c_score_baseline_low = 1.0
        s_score_baseline_low = 1.0
        i_score_baseline_low = 1.0
        a_score_baseline_high = 100.0
        b_score_baseline_high = 20.0
        c_score_baseline_high = 20.0
        s_score_baseline_high = 20.0  # percent
        i_score_baseline_high = 20.0  # percent

        safety_rows = []
        average_score = 0.0
        total_distance = 0.0
        average_a_per_1000 = 0.0
        total_a = 0
        average_b_per_1000 = 0.0
        total_b = 0
        average_c_per_1000 = 0.0
        total_c = 0
        total_s = 0.0
        total_i = datetime.timedelta()

        for vehicle in vehicle_group.vehicles.all():
            #print(vehicle.registration)
            vts = vehicle.trackers.all().order_by('-installed')
            tracker_number = vts[0].tracker
            #print(tracker_number)
            t_key = ndb.Key('tracker', int(tracker_number))
            
            points = []
            points = trackerPoint.query_tracePoints(t_key, startdatetime,
                        enddatetime).filter(trackerPoint.eventCode.IN([4,5,40,41,42])).fetch(MAX_POINTS_PER_DAY)
            
            start_odo = 0.0
            end_odo = 0.0
            a_count = 0
            a_per_1000 = 0.0
            b_count = 0
            b_per_1000 = 0.0
            c_count = 0
            c_per_1000 = 0.0
            s_distance = 0.0
            idle_duration = datetime.timedelta()
            score = 0.0
            distance = 0.0
            keyon_time = None
            duration = datetime.timedelta()

            # TODO must add duration, idle and speed 

            if len(points) > 0:
                for point in points:
                    # Look for 1st key on and record ODO
                    # Also record time at each keyon so we can calc driving duration
                    if (point.eventCode == 4):
                        keyon_time = point.updateDateTime
                        if (start_odo == 0):
                            start_odo = point.getODO()  # ODO in meters

                    # Look for final key off and record ODO
                    # Also record idle duration for each trip
                    # Also record speeding distnace for trip
                    elif (point.eventCode == 5):
                        end_odo = point.getODO()  # ODO in meters
                        idle_duration += datetime.timedelta(seconds=point.getIdleDurationSeconds())
                        s_distance += point.getSpeedingDistance()
                        if keyon_time is not None:
                            duration += (point.updateDateTime - keyon_time)
                            keyon_time = None

                    # Deal with ABC points
                    elif (point.eventCode == 40):
                        a_count += 1
                    elif (point.eventCode == 41):
                        b_count += 1
                    elif (point.eventCode == 42):
                        c_count += 1

            # Calculate distance (in meters)
            if (start_odo != 0) and (end_odo != 0):
                if (end_odo > start_odo):
                    distance = end_odo - start_odo # in meters
            
            # Convert distances to km
            distance = distance / 1000.0
            s_distance = s_distance / 1000.0

            # Calculate ABC per_1000's
            if (distance > 0):
                scale = 1000.0 / distance
                a_per_1000 = a_count * scale
                b_per_1000 = b_count * scale
                c_per_1000 = c_count * scale

            # Calculate scores.  Eaach component can add up to it's 'weight' to the score
            score += calcScoreComponent(a_per_1000, a_score_baseline_low, a_score_baseline_high, weight_a)
            score += calcScoreComponent(b_per_1000, b_score_baseline_low, b_score_baseline_high, weight_b)
            score += calcScoreComponent(c_per_1000, c_score_baseline_low, b_score_baseline_high, weight_c)
            if (distance > 0):
                score += calcScoreComponent((s_distance / distance), s_score_baseline_low, s_score_baseline_high, weight_s)
            else:
                score += weight_s
            if (duration.total_seconds() > 0):
                score += calcScoreComponent((idle_duration.total_seconds() / duration.total_seconds()), i_score_baseline_low, i_score_baseline_high, weight_i)
            else:
                score += weight_i
            safety_rows.append(BehaviourSafetyABCVehicleRow(vehicleId=vehicle.id,
                                                            vehicleName=vehicle.registration,
                                                            score=score,
                                                            distance=distance,
                                                            duration=duration,
                                                            aPerThousand=a_per_1000,
                                                            aCount=a_count,
                                                            bPerThousand=b_per_1000,
                                                            bCount=b_count,
                                                            cPerThousand=c_per_1000,
                                                            cCount=c_count,
                                                            speedingDistance=s_distance,
                                                            idleDuration=idle_duration,
                                                        ))
            average_score += score
            total_distance += distance
            total_a += a_count
            total_b += b_count
            total_c += c_count
            total_s += s_distance
            total_i += idle_duration

        # Calculate totals
        if len(safety_rows) > 0:
            average_score = average_score / len(safety_rows)
            # Calculate ABC per_1000's
            if (total_distance > 0):
                scale = 1000.0 / total_distance
                average_a_per_1000 = total_a * scale
                average_b_per_1000 = total_b * scale
                average_c_per_1000 = total_c * scale

        safety = BehaviourSafetyABCVehicle(vehicleGroupId=vehicle_group_id, 
                                           vehicleGroupName=vehicle_group.name,
                                           startDateTime=startdatetime,
                                           endDateTime=enddatetime,
                                           weightA=weight_a,
                                           weightB=weight_b,
                                           weightC=weight_c,
                                           weightS=weight_s,
                                           weightI=weight_i,
                                           averageScore=average_score,
                                           totalDistance=total_distance,
                                           averageAPerThousand=average_a_per_1000,
                                           totalACount=total_a,
                                           averageBPerThousand=average_b_per_1000,
                                           totalBCount=total_b,
                                           averageCPerThousand=average_c_per_1000,
                                           totalCCount=total_c,
                                           totalSpeedingDistance=total_s,
                                           totalIdleDuration=total_i,
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
        except VehicleGroup.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except exceptions.MultipleObjectsReturned:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(vehicle_group)

        # In future pull these weights from a config
        weight_ldw = 17.0
        weight_hw = 16.0
        weight_ucw = 17.0
        weight_fcw = 17.0
        weight_pdz = 17.0
        weight_s = 16.0
        ldw_score_baseline_low = 2.0
        hw_score_baseline_low = 20.0
        ucw_score_baseline_low = 2.0
        fcw_score_baseline_low = 2.0
        pdz_score_baseline_low = 2.0
        s_score_baseline_low = 2.0
        ldw_score_baseline_high = 100.0
        hw_score_baseline_high = 300.0
        ucw_score_baseline_high = 100.0
        fcw_score_baseline_high = 100.0
        pdz_score_baseline_high = 100.0
        s_score_baseline_high = 100.0

        safety_rows = []
        average_score = 0.0
        total_distance = 0.0
        average_ldw_per_1000 = 0.0
        total_ldw = 0
        average_hw_per_1000 = 0.0
        total_hw = 0
        average_ucw_per_1000 = 0.0
        total_ucw = 0
        average_fcw_per_1000 = 0.0
        total_fcw = 0
        average_pdz_per_1000 = 0.0
        total_pdz = 0
        average_s_per_1000 = 0.0
        total_s = 0

        for vehicle in vehicle_group.vehicles.all():
            #print(vehicle.registration)
            vts = vehicle.trackers.all().order_by('-installed')
            tracker_number = vts[0].tracker
            #print(tracker_number)
            t_key = ndb.Key('tracker', int(tracker_number))
            
            points = []
            points = trackerPoint.query_tracePoints(t_key, startdatetime,
                                enddatetime).filter(trackerPoint.eventCode.IN([4,5,151,152,153,154,155,156,157])).fetch(MAX_POINTS_PER_DAY)
            
            start_odo = 0.0
            end_odo = 0.0
            ldw_count = 0
            ldw_per_1000 = 0.0
            hw_count = 0
            hw_per_1000 = 0.0
            ucw_count = 0
            ucw_per_1000 = 0.0
            fcw_count = 0
            fcw_per_1000 = 0.0
            pdz_count = 0
            pdz_per_1000 = 0.0
            s_count = 0
            s_per_1000 = 0.0
            score = 0.0
            distance = 0.0
            
            if len(points) > 0:
                for point in points:
                    #print(point)

                    # Look for 1st key on and record ODO
                    if (point.eventCode == 4):
                        if (start_odo == 0):
                            start_odo = point.getODO()
                            #if (point.accum0 != 0):  # Use vehicle ODO if it exists
                            #    start_odo = point.accum0
                            #else:  # Otherwise use GPS ODO (accum1 where supported)
                            #    start_odo = point.accum1

                    # Look for final key off and record ODO
                    elif (point.eventCode == 5):
                        end_odo = point.getODO()
                        #if (point.accum0 != 0):  # Use vehicle ODO if it exists
                        #    end_odo = point.accum0
                        #else:  # Otherwise use GPS ODO (accum1 where supported)
                        #    end_odo = point.accum1

                    # Deal with Mobileye activation points
                    elif (point.eventCode == 151):  # LDW left
                        ldw_count += 1
                    elif (point.eventCode == 152):  # LDW right
                        ldw_count += 1
                    elif (point.eventCode == 153):  # HW1
                        hw_count += 1
                    elif (point.eventCode == 154):  # TSR
                        s_count += 1
                    elif (point.eventCode == 155):  # UFCW
                        ucw_count += 1
                    elif (point.eventCode == 156):  # FCW+PCW
                        fcw_count += 1
                    elif (point.eventCode == 157):  # PDZ
                        pdz_count += 1

            # Calculate distance
            if (start_odo != 0) and (end_odo != 0):
                if (end_odo > start_odo):
                    distance = end_odo - start_odo  # in meters
            # Convert distance to km
            distance = distance / 1000.0

            # Calculate activations per_1000's
            if (distance > 0):
                scale = 1000.0 / distance
                ldw_per_1000 = ldw_count * scale
                hw_per_1000 = hw_count * scale
                s_per_1000 = s_count * scale
                ucw_per_1000 = ucw_count * scale
                fcw_per_1000 = fcw_count * scale
                pdz_per_1000 = pdz_count * scale

            # Calculate scores
            score += calcScoreComponent(ldw_per_1000, ldw_score_baseline_low, ldw_score_baseline_high, weight_ldw)
            score += calcScoreComponent(hw_per_1000, hw_score_baseline_low, hw_score_baseline_high, weight_hw)
            score += calcScoreComponent(s_per_1000, s_score_baseline_low, s_score_baseline_high, weight_s)
            score += calcScoreComponent(ucw_per_1000, ucw_score_baseline_low, ucw_score_baseline_high, weight_ucw)
            score += calcScoreComponent(fcw_per_1000, fcw_score_baseline_low, fcw_score_baseline_high, weight_fcw)
            score += calcScoreComponent(pdz_per_1000, pdz_score_baseline_low, pdz_score_baseline_high, weight_pdz)

            safety_rows.append(BehaviourSafetyMobileEyeVehicleRow(vehicleId=vehicle.id,
                                                                  vehicleName=vehicle.registration,
                                                                  score=score,
                                                                  distance=distance,
                                                                  ldwPerThousand=ldw_per_1000,
                                                                  ldwCount=ldw_count,
                                                                  hwPerThousand=hw_per_1000,
                                                                  hwCount=hw_count,
                                                                  ucwPerThousand=ucw_per_1000,
                                                                  ucwCount=ucw_count,
                                                                  fcwPerThousand=fcw_per_1000,
                                                                  fcwCount=fcw_count,
                                                                  pdzPerThousand=pdz_per_1000,
                                                                  pdzCount=pdz_count,
                                                                  sPerThousand=s_per_1000,
                                                                  sCount=s_count,
                                                                  ))
            average_score += score
            total_distance += distance
            total_ldw += ldw_count
            total_hw += hw_count
            total_ucw += ucw_count
            total_fcw += fcw_count
            total_pdz += pdz_count
            total_s += s_count

        # Calculate totals
        if len(safety_rows) > 0:
            average_score = average_score / len(safety_rows)
            # Calculate ABC per_1000's
            if (total_distance > 0):
                scale = 1000.0 / total_distance
                average_ldw_per_1000 = total_ldw * scale
                average_hw_per_1000 = total_hw * scale
                average_ucw_per_1000 = total_ucw * scale
                average_fcw_per_1000 = total_fcw * scale
                average_pdz_per_1000 = total_pdz * scale
                average_s_per_1000 = total_s * scale

        safety = BehaviourSafetyMobileEyeVehicle(vehicleGroupId=vehicle_group_id, 
                                                 vehicleGroupName=vehicle_group.name,
                                                 startDateTime=startdatetime,
                                                 endDateTime=enddatetime,
                                                 weightLDW=weight_ldw,
                                                 weightHW=weight_hw,
                                                 weightUCW=weight_ucw,
                                                 weightFCW=weight_fcw,
                                                 weightPDZ=weight_pdz,
                                                 weightS=weight_s,
                                                 averageScore=average_score,
                                                 totalDistance=total_distance,
                                                 averageLDWPerThousand=average_ldw_per_1000,
                                                 totalLDWCount=total_ldw,
                                                 averageHWPerThousand=average_hw_per_1000,
                                                 totalHWCount=total_hw,
                                                 averageUCWPerThousand=average_ucw_per_1000,
                                                 totalUCWCount=total_ucw,
                                                 averageFCWPerThousand=average_fcw_per_1000,
                                                 totalFCWCount=total_fcw,
                                                 averagePDZPerThousand=average_pdz_per_1000,
                                                 totalPDZCount=total_pdz,
                                                 averageSPerThousand=average_s_per_1000,
                                                 totalSCount=total_s,
                                                 )
        safety.rows = safety_rows
        serializer = serializers.BehaviourSafetyMobileEyeVehicleSerializer(instance=safety)
        return Response(serializer.data)
