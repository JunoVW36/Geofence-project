# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-23 17:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_vehicle_check', '0002_auto_20171122_2253'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuestionDefinitionAnswers',
            new_name='QuestionDefinitionAnswer',
        ),
        migrations.RenameModel(
            old_name='QuestionResponses',
            new_name='QuestionResponse',
        ),
    ]
