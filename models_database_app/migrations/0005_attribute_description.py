# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-16 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_database_app', '0004_owner_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]