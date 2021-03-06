# -*- coding: utf-8 -*-
# Generated by Django 1.11a1 on 2017-07-04 12:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_cust_veh', '0002_auto_20170704_1220'),
        ('datalive_auth', '0002_auto_20170627_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPrefs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_zone', models.CharField(default='Europe/London', max_length=64)),
                ('units_distance', models.CharField(choices=[('MLS', 'Miles'), ('KMS', 'Kilometers')], default='MLS', max_length=3)),
                ('units_volume', models.CharField(choices=[('GAL', 'Gallons'), ('LTR', 'Litres')], default='GAL', max_length=3)),
                ('units_fuel_econ', models.CharField(choices=[('MPG', 'Miles per gallon'), ('LPK', 'Litres per 100km')], default='MPG', max_length=3)),
            ],
        ),
        migrations.AddField(
            model_name='dataliveuser',
            name='customers',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_customers', to='datalive_cust_veh.Customer'),
        ),
        migrations.AddField(
            model_name='dataliveuser',
            name='vehicle_groups',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_vehicle_groups', to='datalive_cust_veh.VehicleGroup'),
        ),
        migrations.AlterField(
            model_name='dataliveuser',
            name='short_name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='userprefs',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
