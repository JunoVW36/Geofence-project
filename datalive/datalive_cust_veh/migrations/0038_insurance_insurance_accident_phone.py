# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-12 21:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_cust_veh', '0037_insurance_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurance',
            name='insurance_accident_phone',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
