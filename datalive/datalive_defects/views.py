# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, views, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Defect, EquipmentDefinition, EquipmentDefinitionFault
#from datalive_settings.models import GlobalSolarVistaSettings, GlobalDefectSettings
from .serializers import *
from services.email_service import EmailService

from datalive_auth.permissions import IsCustomer, IsUser, IsVehicle


class DefectListView(generics.ListCreateAPIView):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    permission_classes = (IsUser, )

    def get_queryset(self):
        return Defect.objects.all()


class DefectListCreate(views.APIView):
    permission_classes = (IsUser, )

    def get(self, request, format=None):

        defects = Defect.objects.all()
        serializer = DefectSerializer(defects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = DefectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('**************')
        print(serializer)
        serializer.save()
      #  email = DefectSettings.confirmation_email
        user = request.user
        EmailService().send_defect_notification_email(user, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# # a view for all defects
# class DefectView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsUser, )
#     queryset = Defect.objects.all()
#     #serializer_class = DefectSerializer
#     # permission_classes = (IsCustomer, )


class EquipmentListView(generics.ListCreateAPIView):
    permission_classes = (IsVehicle, )

    def get(self, request, format=None):
        print('EquipmentListView')
        print(request.user)
        equipments = EquipmentDefinition.objects.all()
        print('Get Equipment ')
        print(equipments)
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data)


class FaultListView(generics.ListCreateAPIView):
    permission_classes = (IsVehicle, )

    def get(self, request, format=None):
        faults = EquipmentDefinitionFault.objects.all()
        serializer = FaultSerializer(faults, many=True)
        return Response(serializer.data)


class EquipmentResponseListView(generics.ListCreateAPIView):
    permission_classes = (IsVehicle, )

    def get(self, request, format=None):
        equip_responses = EquipmentResponse.objects.all()
        serializer = EquipmentResponseSerializer(equip_responses, many=True)
        return Response(serializer.data)


