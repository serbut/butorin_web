# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-18 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask_app', '0005_auto_20161118_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
