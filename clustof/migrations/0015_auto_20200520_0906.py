# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-05-20 07:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clustof', '0014_measurement_cluster_size_distribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='lis_deflector_y',
            field=models.FloatField(blank=True, null=True, verbose_name=b''),
        ),
        migrations.AddField(
            model_name='measurement',
            name='lis_deflector_z',
            field=models.FloatField(blank=True, null=True, verbose_name=b''),
        ),
        migrations.AddField(
            model_name='measurement',
            name='lis_electron_energy',
            field=models.FloatField(blank=True, null=True, verbose_name=b''),
        ),
        migrations.AddField(
            model_name='measurement',
            name='lis_filament_current',
            field=models.FloatField(blank=True, null=True, verbose_name=b''),
        ),
        migrations.AddField(
            model_name='measurement',
            name='lis_ion_block',
            field=models.FloatField(blank=True, null=True, verbose_name=b''),
        ),
        migrations.AddField(
            model_name='measurement',
            name='lis_trap_current',
            field=models.FloatField(blank=True, null=True, verbose_name=b''),
        ),
        migrations.AlterField(
            model_name='comment',
            name='measurement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clustof.Measurement'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clustof.Operator'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clustof.Operator'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='chem_pu1_gas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chem_pu1_gas', to='cheminventory.Chemical', verbose_name=b'Chemical PU1 Gas'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='chem_pu1_oven',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chem_pu1_oven', to='cheminventory.Chemical', verbose_name=b'Chemical PU1 Oven'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='chem_pu2_gas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chem_pu2_gas', to='cheminventory.Chemical', verbose_name=b'Chemical PU2 Gas'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='chem_pu2_oven',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chem_pu2_oven', to='cheminventory.Chemical', verbose_name=b'Chemical PU2 Oven'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='is_inlet_gas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='is_inlet_gas', to='cheminventory.Chemical', verbose_name=b'Ion Source Inlet Gas'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='op1', to='clustof.Operator'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='operator2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='op2', to='clustof.Operator'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='operator3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='op3', to='clustof.Operator'),
        ),
        migrations.AlterField(
            model_name='turbopumpstatus',
            name='pump',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clustof.Turbopump'),
        ),
    ]