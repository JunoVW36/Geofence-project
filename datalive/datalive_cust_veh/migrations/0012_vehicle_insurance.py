# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-11-24 14:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_vehicle_help', '0001_initial'),
        ('datalive_cust_veh', '0011_auto_20171124_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='insurance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_vehicle_help.Insurance'),
        ),
    ]
