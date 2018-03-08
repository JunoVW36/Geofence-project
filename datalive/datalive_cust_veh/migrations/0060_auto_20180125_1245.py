# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-25 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_cust_veh', '0059_vehiclemanufacturermodel_vehicle_model_contacts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicleschematic',
            name='views',
        ),
        migrations.RemoveField(
            model_name='vehiclemanufacturermodel',
            name='schematic',
        ),
        migrations.AddField(
            model_name='vehiclemanufacturermodel',
            name='hero_image',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='vehicle-model-hero-images'),
        ),
        migrations.AddField(
            model_name='vehiclemanufacturermodel',
            name='schematics',
            field=models.ManyToManyField(related_name='vehicle_schematic_views', to='datalive_cust_veh.SchematicView'),
        ),
        migrations.AlterField(
            model_name='vehiclemanufacturermodel',
            name='fuel_type',
            field=models.CharField(choices=[('DIE', 'Diesel'), ('PET', 'Petrol'), ('ELE', 'Electric')], default='DIE', max_length=3),
        ),
        migrations.DeleteModel(
            name='VehicleSchematic',
        ),
    ]