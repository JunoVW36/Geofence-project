# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-01 10:02
from __future__ import unicode_literals

import datalive_vehicle_check.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_cust_veh', '0015_merge_20171128_1031'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datalive_vehicle_check', '0012_auto_20171129_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='GateCheckReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, db_index=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('agency', models.NullBooleanField()),
                ('driver_name', models.CharField(max_length=200, null=True)),
                ('notes', models.TextField(blank=True, max_length=700, null=True)),
                ('depot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='depot_gatecheck_reports', to='datalive_cust_veh.VehicleGroup', validators=[datalive_vehicle_check.models.validate_gatecheck_depot])),
                ('hub', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hub_gatecheck_reports', to='datalive_cust_veh.VehicleGroup', validators=[datalive_vehicle_check.models.validate_gatecheck_hub])),
                ('hub_question_responses', models.ManyToManyField(related_name='hub_gatecheck_reports', to='datalive_vehicle_check.QuestionResponse')),
                ('tractor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tractor_gatecheck_reports', to='datalive_cust_veh.Vehicle')),
                ('tractor_photos', models.ManyToManyField(null=True, related_name='tractor_gatecheck_reports', to='datalive_vehicle_check.ReportPhoto')),
                ('tractor_question_responses', models.ManyToManyField(related_name='tractor_gatecheck_reports', to='datalive_vehicle_check.QuestionResponse')),
                ('trailer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trailer_gatecheck_reports', to='datalive_cust_veh.Vehicle')),
                ('trailer_photos', models.ManyToManyField(null=True, related_name='trailer_gatecheck_reports', to='datalive_vehicle_check.ReportPhoto')),
                ('trailer_question_responses', models.ManyToManyField(related_name='trailer_gatecheck_reports', to='datalive_vehicle_check.QuestionResponse')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='questiondefinition',
            name='type',
            field=models.CharField(choices=[('vehicle', 'Vehicle Condition'), ('tractor', 'Tractor Condition'), ('trailer', 'Trailer Condition'), ('hub', 'Hub Condition')], default='vehicle', max_length=8),
        ),
    ]
