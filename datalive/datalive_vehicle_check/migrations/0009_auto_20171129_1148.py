# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-29 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_vehicle_check', '0008_merge_20171129_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='checker_signature',
            field=models.FileField(null=True, upload_to='vehicle-check/signatures/%Y/%m/%d/signature/'),
        ),
        migrations.AlterField(
            model_name='report',
            name='driver_signature',
            field=models.FileField(null=True, upload_to='vehicle-check/signatures/%Y/%m/%d/signature/'),
        ),
    ]