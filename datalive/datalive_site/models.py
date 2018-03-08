# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class GlobalSettings(models.Model):
    """
    Global Defect settings
    """
    send_confirmation_email = models.BooleanField(default=False)
    confirmation_email_address = models.EmailField(max_length=256, blank=False, null=False)
    post_to_solar_vista = models.BooleanField(default=False)
    def __str__(self):
        return self.confirmation_email_address
    

class GlobalSolarVistaSettings(models.Model):
    """
    Global Solar Vista settings
    """
    solar_vista_host = models.CharField(max_length=150)
    solar_vista_path = models.CharField(max_length=150)
    def __str__(self):
        return self.solar_vista_host