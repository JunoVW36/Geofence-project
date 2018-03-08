# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-11-24 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
    ]