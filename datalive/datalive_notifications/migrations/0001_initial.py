# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-14 21:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    # dependencies = [
    #     ('datalive_cust_veh', '0041_auto_20171214_2108'),
    # ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('type', models.CharField(choices=[('panic', 'Panic button')], max_length=16)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='datalive_cust_veh.Vehicle')),
            ],
        ),
    ]
