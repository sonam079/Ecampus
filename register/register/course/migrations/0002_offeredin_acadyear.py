# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-18 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offeredin',
            name='acadYear',
            field=models.CharField(default='', max_length=200),
        ),
    ]
