# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 16:16
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datalive_auth', '0007_auto_20170707_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldUserPassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=1024)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='old_user_pass', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserResetPasswordToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default='5097cddb0d7d2989ad0b0419d0c14223fd6296b363d2eed430ca8dff84b3bcd8', max_length=1024)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('expiration_date', models.DateTimeField(default=datetime.datetime(2017, 7, 12, 16, 16, 17, 319812))),
                ('is_used', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_pass_token', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
