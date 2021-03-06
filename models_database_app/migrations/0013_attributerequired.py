# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-11 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models_database_app', '0012_versionattributerecordchoice'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeRequired',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obj_type', models.CharField(choices=[('MODEL', 'MODEL'), ('VERSION', 'VERSION')], max_length=300)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='required', to='models_database_app.Attribute')),
                ('risk_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='required', to='models_database_app.RiskType')),
            ],
        ),
    ]
