# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-25 07:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_vehicle_check', '0019_auto_20180125_0707'),
        ('datalive_cust_veh', '0056_auto_20180125_0707'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LiveryView',
        ),
        migrations.AddField(
            model_name='vehicleschematic',
            name='views',
            field=models.ManyToManyField(related_name='vehicle_schematic_views', to='datalive_cust_veh.SchematicView'),
        ),
        migrations.AddField(
            model_name='vehiclemanufacturermodel',
            name='manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.VehicleManufacturer'),
        ),
        migrations.AddField(
            model_name='vehiclemanufacturermodel',
            name='schematics',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.VehicleSchematic'),
        ),
        migrations.AddField(
            model_name='schematicview',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.Customer'),
        ),
        migrations.AddField(
            model_name='liveryschematic',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.Customer'),
        ),
        migrations.AddField(
            model_name='liveryschematic',
            name='livery_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.LiveryCategory'),
        ),
        migrations.AddField(
            model_name='liveryschematic',
            name='manufacturer_model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.VehicleManufacturerModel'),
        ),
        migrations.AddField(
            model_name='liveryschematic',
            name='views',
            field=models.ManyToManyField(related_name='livery_schematic_views', to='datalive_cust_veh.SchematicView'),
        ),
        migrations.AddField(
            model_name='liverycategory',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.Customer'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='livery_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datalive_cust_veh.LiveryCategory'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='manufacturer_model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.VehicleManufacturerModel'),
        ),
    ]
