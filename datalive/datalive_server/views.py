# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, views, status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from datalive_auth.permissions import IsServer, IsAdmin
from datalive_defects.models import Defect
from datalive_defects.serializers import *
from datalive_vehicle_check.models import Report, Damage
from datalive_vehicle_check.serializers import *



class DefectListCreate(views.APIView):
    '''
    A view to post Defect data from XLR server
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsServer,)

   
    # def get(self, request, format=None):
    #     defects = Defect.objects.all()
    #     serializer = DefectSerializer(defects, many=True)
    #     #XlrDefectSerializer
    #     return Response(serializer.data)

    def post(self, request, format=None):
        print('User permissions: ')
        print(request.user.permission)
        print('Is Server: ')
        print(request.user.permission.is_server_user)
        serializer = DefectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VehicleCheckListCreate(views.APIView):
    '''
    A view to post Vehicle Check data from XLR server
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        vehicleChecks = Report.objects.all()
        serializer = ReportSerializer(vehicleChecks, many=True)
        #XlrDefectSerializer
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)







class ServerTokenAuthTest(views.APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        # try:
        #     request.auth
        # except request.auth.none:
        #     return Response({'unauthorized'}, status=status.HTTP_401_BAD_REQUEST)
        return Response({'status': 'Ok'})