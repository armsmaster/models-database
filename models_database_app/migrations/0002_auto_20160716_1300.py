# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-16 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_database_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelattribute',
            name='valid_record_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='versionattribute',
            name='valid_record_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
