# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-12-17 12:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask_app', '0013_question_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='likes',
            new_name='rating',
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='author',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='likes',
            new_name='rating',
        ),
    ]
