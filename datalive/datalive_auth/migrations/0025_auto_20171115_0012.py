# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-15 00:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_auth', '0024_auto_20171115_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpermission',
            name='is_server_client1',
        ),
        migrations.AlterField(
            model_name='userresetpasswordtoken',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 16, 0, 11, 59, 659454)),
        ),
    ]