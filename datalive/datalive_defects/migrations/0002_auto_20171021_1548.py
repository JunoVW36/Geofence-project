# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-21 15:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_defects', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DefectSettings',
            new_name='DefectSetting',
        ),
    ]