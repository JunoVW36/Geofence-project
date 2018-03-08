# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-29 12:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datalive_cust_veh', '0045_vehicle_service_due_odo'),
        ('datalive_vehicle_check', '0015_auto_20171203_0839'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditSurveyReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('data', django_mysql.models.JSONField(default=dict)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_reports', to='datalive_cust_veh.VehicleGroup')),
            ],
        ),
        migrations.CreateModel(
            name='AuditSurveyTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('template', django_mysql.models.JSONField(default=dict)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_templates', to='datalive_cust_veh.Customer')),
            ],
        ),
        migrations.AddField(
            model_name='auditsurveyreport',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='datalive_vehicle_check.AuditSurveyTemplate'),
        ),
    ]
