    # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django_mysql.models import JSONField
# from datalive_auth.models import DataliveUser
from datalive_cust_veh.models import Vehicle, Customer

# Create your models here.


# A model to categorise a Geofence 
class GeofenceCategory(models.Model):
    category_name = models.CharField(max_length=200)
    category_colour = models.CharField(max_length=200)
    # user = models.ForeignKey(DataliveUser, null=True, on_delete=models.SET_NULL)
    """ A model to categorise a Geofence 
    """
    def __str__(self):
        return self.category_name


# A model for a Geofence item
class GeofenceBoundingBox(models.Model):
    min_long = models.DecimalField(max_digits=6, decimal_places=2)
    min_lat = models.DecimalField(max_digits=6, decimal_places=2)
    max_long = models.DecimalField(max_digits=6, decimal_places=2)
    max_lat = models.DecimalField(max_digits=6, decimal_places=2)
    """min Longitude , min Latitude , max Longitude , max Latitude E.g. left,bottom,right,top """

# A model for a Geofence item
class Geofence(models.Model):
    GEOFENCE_TYPE_CIRCLE = 'circle'
    GEOFENCE_TYPE_RECT = 'rectangle'
    GEOFENCE_TYPE_POLYGON = 'polygon'

    GEOFENCE_TYPE_CHOICES = (
        (GEOFENCE_TYPE_CIRCLE, 'Circle Geofence'),
        (GEOFENCE_TYPE_RECT, 'Rectangle Geofence'),
        (GEOFENCE_TYPE_POLYGON, 'Polygon Geofence'),
    )

    creation_datetime = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, db_index=True)
    category = models.ForeignKey(GeofenceCategory, null=True, blank=True)
    geofence_type = models.CharField(max_length=10, choices=GEOFENCE_TYPE_CHOICES, default=GEOFENCE_TYPE_CIRCLE)
    coordinates = JSONField()
    bbox =  models.ForeignKey(GeofenceBoundingBox, null=True)
    archived = models.BooleanField(default=False)
    vehicles = models.ManyToManyField(Vehicle, through="GeofenceVehicleMap", null=True)
    """A Geofence should not be deleted but archived"""
    def __str__(self):
        return self.name


class GeofenceNotificationEmail(models.Model):
    """Model to hold a list of email address. These can be assigned to a GeofenceGroups. 
    Can be used for notifications to be sent
    """
    name = models.CharField(max_length=200, db_index=True)
    """Name of contact."""
    email = models.EmailField(max_length=256, blank=False, null=False)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.email

# A model to group Geofences
class GeofenceGroup(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    geofences = models.ManyToManyField(Geofence, null=True)
    """List of Geofences in this group."""
    archived = models.BooleanField(default=False)
    """A Geofences group should not be deleted but archived"""
    notifications_emails = models.ManyToManyField(GeofenceNotificationEmail, blank=True)

    """List of email addresses. Use for their email address for reports to be sent to them"""
    def __str__(self):
        return self.name


class GeofenceVehicleMap(models.Model):
    vehicle = models.ForeignKey(Vehicle, null=True)
    geofence = models.ForeignKey(Geofence, null=True)


class GeofeceGeofenceGroupMap(models.Model):
    notifications_emails = models.ForeignKey(GeofenceNotificationEmail, null=True)
    geofence_group = models.ForeignKey(GeofenceGroup, null=True)


