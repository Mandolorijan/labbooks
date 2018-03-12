# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 07:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wippi', '0003_measurement_fragment'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='nozzle',
            field=models.FloatField(blank=True, default=12, null=True, verbose_name=b'Nozzle Temperature'),
        ),
    ]
