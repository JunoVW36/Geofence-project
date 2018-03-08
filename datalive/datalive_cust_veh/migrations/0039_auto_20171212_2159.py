# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-12 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_cust_veh', '0038_insurance_insurance_accident_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insurance',
            name='policy_document',
        ),
        migrations.RemoveField(
            model_name='insurance',
            name='policy_number',
        ),
        migrations.AddField(
            model_name='insurancepolicynumber',
            name='policy_document',
            field=models.ImageField(blank=True, max_length=256, null=True, upload_to='customer/insurance/'),
        ),
    ]
