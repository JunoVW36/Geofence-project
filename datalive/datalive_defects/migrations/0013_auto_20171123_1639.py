# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-23 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_defects', '0012_auto_20171123_1625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equipmentdefinition',
            old_name='answers',
            new_name='faults',
        ),
        migrations.AlterField(
            model_name='equipmentdefinition',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]