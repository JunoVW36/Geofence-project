# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, views, status, exceptions
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from datalive_auth.permissions import IsCustomer, IsUser, IsVehicle

from datalive_cust_veh.models import Vehicle
from datalive_notifications.models import Notification
from datalive_notifications.serializers import *
from django.conf import settings
import logging
from tasks import daily_vehicle_check_damage_email, mot_expiry_email_notifications
from datetime import timedelta
from django.utils import timezone


class NotificationListCreate(views.APIView):
    permission_classes = (AllowAny, )

    def get(self, request, format=None):

        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):

        serializer = NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('*************')
        print(serializer)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CronMixin(object):
    def check_permissions(self, request):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        logging.warning(request.META)
        if 'HTTP_X_APPENGINE_CRON' not in request.META or request.META['HTTP_X_APPENGINE_CRON'] != 'true':
            raise exceptions.NotAcceptable()


class VehicleCheckDamage(CronMixin, views.APIView):
    permission_classes = (AllowAny, )

    def get(self, request, format=None):

        daily_vehicle_check_damage_email(timezone.now().date()-timedelta(days=1))

        return Response('OK VEHICLE CHECK')


class MotExpiryEmail(CronMixin, views.APIView):
    permission_classes = (AllowAny, )

    def get(self, request, format=None):

        mot_expiry_email_notifications()

        return Response('OK MOT EXPIRY')

# a view for all Notifications
# class NotificationView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsUser, )
#     queryset = Notification.objects.all()