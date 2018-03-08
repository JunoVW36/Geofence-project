# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.

admin.autodiscover()


admin.site.register(GeofenceCategory)
admin.site.register(Geofence)
admin.site.register(GeofenceGroup)
admin.site.register(GeofenceBoundingBox)
admin.site.register(GeofenceVehicleMap)
