# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-07 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_cust_veh', '0046_auto_20180106_2035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='gross_vehicle_weight',
        ),
        migrations.AlterField(
            model_name='liveryview',
            name='view_name',
            field=models.CharField(choices=[('FRNT', 'Front'), ('DRVI', 'Driver'), ('REAR', 'Rear'), ('PASS', 'Passenger')], max_length=10, null=True),
        ),
    ]
