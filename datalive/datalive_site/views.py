# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, views, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import *
#from datalive_settings.models import SolarVistaSettings, DefectSettings
from .serializers import *

from datalive_auth.permissions import IsCustomer, IsUser, IsVehicle



class SettingsListView(generics.ListCreateAPIView):
    serializer_class = DefectSettingsSerializer
    permission_classes = (IsUser, )

    def get_queryset(self):
        return GlobalDefectSettings.objects.all()