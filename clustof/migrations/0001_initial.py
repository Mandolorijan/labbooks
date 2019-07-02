# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('text', models.TextField(max_length=3000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CurrentSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tof_settings_file', models.CharField(max_length=1500, verbose_name=b'TOF Settings File')),
                ('tof_settings_file_time', models.DateTimeField()),
                ('data_filename', models.CharField(default=b'D:\\Data\\', max_length=1500, verbose_name=b'Filename')),
                ('data_filename_time', models.DateTimeField()),
                ('pressure_cs', models.FloatField(default=4e-05, verbose_name=b'Pressure CS')),
                ('pressure_cs_time', models.DateTimeField()),
                ('pressure_pu1', models.FloatField(default=3e-06, verbose_name=b'Pressure PU1')),
                ('pressure_pu1_time', models.DateTimeField()),
                ('pressure_pu2', models.FloatField(default=1e-06, verbose_name=b'Pressure PU2')),
                ('pressure_pu2_time', models.DateTimeField()),
                ('pressure_ion', models.FloatField(default=2e-08, verbose_name=b'Pressure ION')),
                ('pressure_ion_time', models.DateTimeField()),
                ('pressure_tof', models.FloatField(default=3e-07, verbose_name=b'Pressure TOF')),
                ('pressure_tof_time', models.DateTimeField()),
                ('temperature_he', models.FloatField(default=9.0, verbose_name=b'He Temperature')),
                ('temperature_he_time', models.DateTimeField()),
                ('electron_energy_set', models.FloatField(null=True, verbose_name=b'Electron Energy (for MS)', blank=True)),
                ('electron_energy_set_time', models.DateTimeField()),
                ('ion_block', models.FloatField()),
                ('ion_block_time', models.DateTimeField()),
                ('pusher', models.FloatField()),
                ('pusher_time', models.DateTimeField()),
                ('wehnelt', models.FloatField()),
                ('wehnelt_time', models.DateTimeField()),
                ('extraction_1', models.FloatField()),
                ('extraction_1_time', models.DateTimeField()),
                ('extraction_2', models.FloatField()),
                ('extraction_2_time', models.DateTimeField()),
                ('deflector_1', models.FloatField()),
                ('deflector_1_time', models.DateTimeField()),
                ('deflector_2', models.FloatField()),
                ('deflector_2_time', models.DateTimeField()),
                ('filament_current', models.FloatField()),
                ('filament_current_time', models.DateTimeField()),
                ('trap_current', models.FloatField()),
                ('trap_current_time', models.DateTimeField()),
                ('oven_1_temperature', models.FloatField(null=True, blank=True)),
                ('oven_1_temperature_time', models.DateTimeField()),
                ('oven_1_power', models.FloatField(null=True, blank=True)),
                ('oven_1_power_time', models.DateTimeField()),
                ('oven_2_temperature', models.FloatField(null=True, blank=True)),
                ('oven_2_temperature_time', models.DateTimeField()),
                ('oven_2_power', models.FloatField(null=True, blank=True)),
                ('oven_2_power_time', models.DateTimeField()),
                ('polarity', models.CharField(default=b'NEG', max_length=3, choices=[(b'NEG', b'Negative'), (b'POS', b'Positive'), (b'OLD', b'Unknown (Old File)')])),
                ('polarity_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('attachment', models.FileField(default=b'', upload_to=b'clustof/techjournal/', blank=True)),
            ],
            options={
                'ordering': ['-time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('tof_settings_file', models.CharField(max_length=1500, verbose_name=b'TOF Settings File')),
                ('data_filename', models.CharField(default=b'D:\\Data\\', max_length=1500, verbose_name=b'Filename')),
                ('rating', models.IntegerField(default=3, null=True, blank=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('scantype', models.CharField(default=b'MS', max_length=20, choices=[(b'ES', b'Energyscan'), (b'MS', b'Mass Spectrum'), (b'TS', b'Temperature-Scan'), (b'PS', b'Pressure-Scan'), (b'OLD', b'Unknown (Old File)')])),
                ('pressure_cs', models.FloatField(default=4e-05, verbose_name=b'Pressure CS')),
                ('pressure_pu1', models.FloatField(default=3e-06, verbose_name=b'Pressure PU1')),
                ('pressure_pu2', models.FloatField(default=1e-06, verbose_name=b'Pressure PU2')),
                ('pressure_ion', models.FloatField(default=2e-08, verbose_name=b'Pressure ION')),
                ('pressure_tof', models.FloatField(default=3e-07, verbose_name=b'Pressure TOF')),
                ('stag_pressure_he', models.FloatField(default=25, verbose_name=b'He Stagnation Pressure')),
                ('temperature_he', models.FloatField(default=9.0, verbose_name=b'He Temp')),
                ('nozzle_diameter', models.FloatField(default=0.4)),
                ('electron_energy_set', models.FloatField(null=True, verbose_name=b'Electron Energy set on Power Supply (for MS)', blank=True)),
                ('real_electron_energy', models.FloatField(null=True, verbose_name=b'Real Electron Energy (for MS)', blank=True)),
                ('ion_block', models.FloatField()),
                ('pusher', models.FloatField()),
                ('wehnelt', models.FloatField()),
                ('extraction_1', models.FloatField()),
                ('extraction_2', models.FloatField()),
                ('deflector_1', models.FloatField(verbose_name=b'Deflector oben/unten')),
                ('deflector_2', models.FloatField(verbose_name=b'Deflector links/rechts')),
                ('filament_current', models.FloatField()),
                ('trap_current', models.FloatField()),
                ('housing_current', models.FloatField(null=True, blank=True)),
                ('oven_1_temperature', models.FloatField(null=True, blank=True)),
                ('oven_1_power', models.FloatField(null=True, blank=True)),
                ('oven_2_temperature', models.FloatField(null=True, blank=True)),
                ('oven_2_power', models.FloatField(null=True, blank=True)),
                ('faraday_cup', models.FloatField(null=True, blank=True)),
                ('flagged', models.BooleanField(default=False)),
                ('substance', models.TextField(max_length=1500)),
                ('polarity', models.CharField(default=b'NEG', max_length=3, choices=[(b'NEG', b'Negative'), (b'POS', b'Positive'), (b'OLD', b'Unknown (Old File)')])),
                ('evaluated_by', models.CharField(max_length=20, blank=True)),
                ('evaluation_file', models.FileField(default=b'', upload_to=b'clustof/evaluations/', blank=True)),
            ],
            options={
                'ordering': ['-time'],
                'get_latest_by': 'time',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Turbopump',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100, blank=True)),
                ('purchase_date', models.DateField(null=True, blank=True)),
                ('service_date', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TurbopumpStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('pump', models.ForeignKey(to='clustof.Turbopump')),
            ],
            options={
                'verbose_name_plural': 'Turbopump Status',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='measurement',
            name='operator',
            field=models.ForeignKey(to='clustof.Operator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='journalentry',
            name='operator',
            field=models.ForeignKey(to='clustof.Operator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='measurement',
            field=models.ForeignKey(to='clustof.Measurement'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='operator',
            field=models.ForeignKey(to='clustof.Operator'),
            preserve_default=True,
        ),
    ]