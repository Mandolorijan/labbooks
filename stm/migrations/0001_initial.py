# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-22 15:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('snowball', '0009_auto_20180312_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('img_fwd_up', models.FileField(max_length=400, upload_to='stm/images/fwd/up/%Y/%m/%d/', verbose_name='Image Fwd/Up')),
                ('img_bwd_up', models.FileField(max_length=400, upload_to='stm/images/bwd/down/%Y/%m/%d/', verbose_name='Image Bwd/Up')),
                ('img_fwd_down', models.FileField(max_length=400, upload_to='stm/images/fwd/up/%Y/%m/%d/', verbose_name='Image Fwd/Down')),
                ('img_bwd_down', models.FileField(max_length=400, upload_to='stm/images/bwd/down/%Y/%m/%d/', verbose_name='Image Bwd/Down')),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('experiment_type', models.CharField(choices=[('STM', 'STM'), ('STS', 'STS'), ('STA', 'STA')], default='STM', max_length=3)),
                ('tip_type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('snowball_measurement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='snowball.Measurement')),
            ],
        ),
        migrations.CreateModel(
            name='StandardOperatingProcedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=5000)),
                ('manual', models.FileField(blank=True, upload_to='stm/sop/', verbose_name='Manual')),
            ],
        ),
        migrations.AddField(
            model_name='measurement',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stm.Operator'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stm.Sample'),
        ),
        migrations.AddField(
            model_name='image',
            name='measurement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stm.Measurement'),
        ),
    ]