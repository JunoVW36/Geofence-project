# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-08 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_cust_veh', '0048_vehicle_gross_vehicle_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='lease_company',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
