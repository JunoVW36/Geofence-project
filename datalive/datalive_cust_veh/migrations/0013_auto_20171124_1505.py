# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-11-24 15:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_cust_veh', '0012_vehicle_insurance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('address', models.CharField(blank=True, max_length=1024, null=True)),
                ('phone', models.CharField(blank=True, max_length=256, null=True)),
                ('url', models.URLField(max_length=256)),
                ('policy_number', models.CharField(max_length=255)),
                ('policy_document_url', models.URLField(max_length=256)),
            ],
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='insurance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datalive_cust_veh.Insurance'),
        ),
    ]
