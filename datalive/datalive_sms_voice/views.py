# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics, views, status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from datalive_auth.permissions import IsServer, IsAdmin
from datalive_cust_veh.models import Vehicle
from datalive_notifications.models import Notification
from datalive_notifications.serializers import *
from django.conf import settings

# Twilio SDK
from twilio.twiml.messaging_response import MessagingResponse


class SmsService(object):

    def sendSms(self, to, message):
        token = settings.TWILIO_AUTH_TOKEN
        sid = settings.TWILIO_ACCOUNT_SID
        number = settings.TWILIO_NUMBER
        print(token, sid, number)
        client = Client(sid, token)
        client.messages.create(
            to= to,
            from_= number,
            body= message,
        )


class ReceivePanicButtonMessageView(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        # TODO: change request.data.get('text') to parse XML object from TWILIO
        print(request.data)
        message_text = request.data.get('Body')
        message_sid = request.data.get('SmsMessageSid')
        message_from = request.data.get('From')
        print(message_from)
        message_from = message_from[1:]
        print('AFTER')
        print(message_from)
        print('message_text: ' + str(message_text))
        # vehicle = Vehicle.objects.filter().extra(where=["%s LIKE CONCAT('%%',registration,'%%')"], params=[message_text]).first()
        # # check for vehicle from text body

        # if vehicle:
        #     print('YES a vehicle has been found!!!!')
        # else:
        #     # vehicle = None
        #     vehicle = Vehicle.objects.get(mobile_number=message_from)
        
        try:
            vehicle = Vehicle.objects.get(mobile_number=message_from)
        except Vehicle.DoesNotExist:
            vehicle = None

        print('VEHICLE:')
        print(vehicle)
        notification = Notification(vehicle=vehicle, source=Notification.NOTIFICATION_SOURCES_SMS, type=Notification.NOTIFICATION_TYPE_PANIC, text=message_text, message_sid=message_sid)

        data = NotificationSerializer(notification).data
        # Save notification
        notification.save()

        # Notifiy by email and text
        message="PANIC NOTIFICATION! Message text: " + str(message_text) + ' | VehicleID: ' + str(vehicle) + '. | Notification Type: ' + str(notification.type) + '. | From: ' + str(message_from)
        
        # numbers 
        # Matt: 447968426522
        # Pete: 447979128473
        # Shereen Hayward DPD : 447717304805
        numbers = ['447919078482', '447968426522', '447979128473', '447717304805']
        # Send notifications to the above array
        for s in numbers:
            print s
            SmsService().sendSms(s, message)
            
        Notification.notify_email(notification)
       
        """Respond to incoming http request from SMS service. Just a success 200 HTPP status"""
        print('request form http')
        return Response(status=status.HTTP_200_OK)








