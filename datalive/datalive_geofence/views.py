# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, views, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Geofence, GeofenceBoundingBox, GeofenceBoundingBox, GeofenceGroup, GeofenceCategory
from .serializers import *
from services.email_service import EmailService

from datalive_auth.permissions import IsCustomer, IsUser, IsVehicle

class GeofenceCategoryView(views.APIView):
    # permission_classes = (IsUser, )
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        """
            description: Show All GeofenceGroups with Geofences information
            @param: None
        """
        geofence_categories = GeofenceCategory.objects.all()
        serializer = GeofenceCategorySerializer(geofence_categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """ 
            description: Add a GeofenceGroup
            @param: GeofenceGroup data
        """
        print ('******************************** \n', request.data)
        serializer = GeofenceCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('*************')
        print ('request:', request.data)
        print(serializer)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GeofenceGroupsView(views.APIView):
    # permission_classes = (IsUser, )

    def allowed_methods(self):
        """
        Return the list of allowed HTTP methods, uppercased.
        """
        self.http_method_names.append("post")
        return [method.upper() for method in self.http_method_names
            if hasattr(self, method)]

    def get(self, request, format=None):
        """
            description: Show All GeofenceGroups with Geofences information
            @param: None
        """
        geofence_groups = GeofenceGroup.objects.all()
        serializer = GeofenceGroupSerializer(geofence_groups, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """ 
            description: Add a GeofenceGroup
            @param: GeofenceGroup data
        """
        serializer = GeofenceGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('*************')
        print(serializer)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GeofencesView(views.APIView):
    # permission_classes = (IsUser, )

    def get(self, request, format=None):
        """
            description: Show All GeofenceGroups with Geofences information
            @param: None
        """
        geofences = Geofence.objects.all()
        serializer = GeofenceSerializer(geofences, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """ 
            description: Add a GeofenceGroup
            @param: GeofenceGroup data
        """
        serializer = GeofenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('*************')
        print(serializer)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

