# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datalive_cust_veh.models import Vehicle, VehicleGroup
from services.email_service import EmailService
from django.conf import settings
from twilio.rest import Client


class Notification(models.Model):
    """Model for storing and send notifications"""

    NOTIFICATION_TYPE_PANIC = 'panic'
    NOTIFICATION_TYPE_DAILY_VEHICLE_CHECK_EMAIL = 'daily_veh_check'
    NOTIFICATION_TYPE_MOT_EXPIRY_EMAIL = 'mot_expiry'
    NOTIFICATION_TYPES = (
        (NOTIFICATION_TYPE_PANIC, 'Panic button'),
        (NOTIFICATION_TYPE_DAILY_VEHICLE_CHECK_EMAIL, 'Daily vehicle check'),
        (NOTIFICATION_TYPE_MOT_EXPIRY_EMAIL, 'MOT expiry'),
    )
    NOTIFICATION_SOURCES_SMS = 'SMS'
    NOTIFICATION_SOURCES = (
        ('SMS', 'Incoming SMS'),
        ('VCE', 'Incoming Voice'),
        ('WEB', 'From Web'),
        ('CRON', 'Cron task'),
    )
    vehicle = models.ForeignKey(Vehicle, related_name='notifications', null=True, blank=True)
    notified_by = models.CharField(max_length=30,  null=True)
    source = models.CharField(choices=NOTIFICATION_SOURCES, max_length=5, default='SMS')
    """ a field to tell where the noftification came from. e.g. web, sms"""
    type = models.CharField(choices=NOTIFICATION_TYPES, max_length=16)
    text = models.TextField()
    message_sid = models.CharField(max_length=42, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return 'Type: %s | Source: %s ' % (str(self.type), str(self.source))
    
    
    def notify_email(self):
       
        if self.type == self.NOTIFICATION_TYPE_PANIC:
            subject = 'NOTIFICATION - Panic Button Alert from ' + str(self.notified_by)
            body = 'Panic message recieved: | Text message:' + str(self.text) + '. | VehicleID: ' + str(self.vehicle) + '. | Date: ' + str(self.date) + ', ' + str(self.time) + 'From: ' + str(self.notified_by)
            

            emails = ['brian@thejustbrand.co.uk', 'nathan@thejustbrand.co.uk', 'matt.johnson@handsfree.co.uk', 'pete.oughton@handsfree.co.uk', 'shereen.hayward@dpdgroup.co.uk' ]
            # Send notifications to the above array
            for s in emails:
                print s
                EmailService().send_generic_email(s, subject, body)

            pass

    def notify_phone(self):
        # TODO: implement phone number notifications
        if self.type == self.NOTIFICATION_TYPE_PANIC:
            print('notify_phone-------')
            print(self.__dict__)
            to= '447919078482'
            message="NOTIFICATION - This message was sent:" + str(self.text) + 'VehicleID: ' + str(self.vehicle) + 'Notification Type: ' + str(self.type)
            SmsService().sendSms(to, message)
           
            pass