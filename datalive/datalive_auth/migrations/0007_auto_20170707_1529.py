# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 15:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_auth', '0006_auto_20170707_1416'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpermission',
            old_name='is_customer_user',
            new_name='is_customer',
        ),
    ]
