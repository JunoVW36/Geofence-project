# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-13 18:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_auth', '0015_auto_20171112_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userresetpasswordtoken',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 14, 18, 10, 25, 87469)),
        ),
    ]
