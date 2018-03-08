# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-03 22:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datalive_cust_veh', '0006_auto_20171028_0843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Damage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('scratch', 'Scratch'), ('crack', 'Crack'), ('missing', 'Missing'), ('dent', 'Dent')], max_length=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('x', models.FloatField(max_length=10)),
                ('y', models.FloatField(max_length=10)),
                ('bx', models.FloatField(max_length=10)),
                ('by', models.FloatField(max_length=10)),
                ('bw', models.FloatField(max_length=10)),
                ('bh', models.FloatField(max_length=10)),
                ('status', models.CharField(choices=[('NEW', 'New damage'), ('FIX', 'Fixed damage')], default='NEW', max_length=5)),
                ('been_fixed', models.BooleanField(verbose_name=False)),
                ('fixed_date', models.DateTimeField(blank=True, null=True)),
                ('rep_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.Vehicle')),
                ('view', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.LiveryView')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(auto_now_add=True, db_index=True)),
                ('creation_time', models.TimeField(auto_now_add=True)),
                ('report_class', models.CharField(choices=[('CHK', 'Vehicle Check Complete'), ('SHOP', 'Not Checked - Vehicle in workshop'), ('ROAD', 'Not Checked - Vehicle on the road'), ('DEPOT', 'Not Checked - Vehicle at other depot')], default='CHK', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='ReportDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('STD', 'Standard Vehicle Check Complete'), ('AUD', 'Auditor Vehicle Check of Vehicle'), ('HND', 'ODF handover check')], default='STD', max_length=5)),
                ('checker_name', models.CharField(max_length=200)),
                ('checker_signature', models.ImageField(upload_to='vehicle-reports/%Y/%m/%d/signature/')),
                ('driver_name', models.CharField(max_length=200)),
                ('driver_signature', models.ImageField(upload_to='vehicle-reports/%Y/%m/%d/signature/')),
                ('notes', models.TextField(blank=True, max_length=700, null=True)),
                ('odometer', models.IntegerField(blank=True, null=True)),
                ('defect_details', models.TextField(blank=True, max_length=700, null=True)),
                ('send_email_flag', models.BooleanField(verbose_name=True)),
                ('depot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.VehicleGroup')),
                ('fixed_damage', models.ManyToManyField(blank=True, related_name='fixed_damages', to='datalive_vehicle_check.Damage')),
                ('new_damage', models.ManyToManyField(blank=True, related_name='new_damages', to='datalive_vehicle_check.Damage')),
            ],
        ),
        migrations.CreateModel(
            name='ReportPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='vehicle-reports/%Y/%m/%d/')),
            ],
        ),
        migrations.AddField(
            model_name='reportdetail',
            name='photos',
            field=models.ManyToManyField(blank=True, to='datalive_vehicle_check.ReportPhoto'),
        ),
        migrations.AddField(
            model_name='report',
            name='report_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datalive_vehicle_check.ReportDetail'),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='report',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.Vehicle'),
        ),
    ]