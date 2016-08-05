# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-05 21:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models_database_app', '0007_auto_20160718_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='model',
            name='risk_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='models', to='models_database_app.RiskType'),
        ),
    ]
