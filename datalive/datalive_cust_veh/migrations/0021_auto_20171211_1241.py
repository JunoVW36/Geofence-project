# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-11 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_cust_veh', '0020_auto_20171210_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address1',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]