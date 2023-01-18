# Generated by Django 3.0.8 on 2020-07-03 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cheminventory', '0002_auto_20200703_1603'),
        ('clustof', '0001_squashed_0016_auto_20200520_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentsetting',
            name='data_filename',
            field=models.CharField(default='D:\\Data\\', max_length=1500, verbose_name='Filename'),
        ),
        migrations.AlterField(
            model_name='currentsetting',
            name='electron_energy_set',
            field=models.FloatField(blank=True, null=True, verbose_name='Electron Energy (for MS)'),
        ),
        migrations.AlterField(
            model_name='currentsetting',
            name='polarity',
            field=models.CharField(choices=[('NEG', 'Negative'), ('POS', 'Positive'), ('OLD', 'Unknown (Old File)')], default='NEG', max_length=3),
        ),
        migrations.AlterField(
            model_name='currentsetting',
            name='pressure_cs',
            field=models.FloatField(default=4e-05, verbose_name='Pressure CS'),
        ),
        migrations.AlterField(
            model_name='currentsetting',
            name='pressure_ion',
            field=models.FloatField(default=2e-08, verbose_name='Pressure ION'),
        ),
        migrations.AlterField(
            model_name='currentsetting',
            name='pressure_pu1',
            field=models.FloatField(default=3e-06, verbose_name='Pressure PU1'),
        ),
        migrations.AlterField(
            model_name='currentsetting',
            name='pressure_pu2',
            field=models.FloatField(default=1e-06, verbose_name='Pressure PU2'),
        ),
        migrations.AlterField(
            model_name='currentsetting',
            name='pressure_tof',
            field=models.FloatField(default=3e-07, verbose_name='Pressure TOF'),
        ),
        migrations.AlterField(
            model_name='currentsetting',
            name='temperature_he',
            field=models.FloatField(default=9.0, verbose_name='He Temperature'),
        ),
        migrations.AlterField(
            model_name='currentsetting',
            name='tof_settings_file',
            field=models.CharField(max_length=1500, verbose_name='TOF Settings File'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='attachment',
            field=models.FileField(blank=True, default='', upload_to='clustof/techjournal/'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='written_notes',
            field=models.ImageField(blank=True, upload_to='clustof/techjournal/notes/'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='chem_pu1_gas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chem_pu1_gas', to='cheminventory.Chemical', verbose_name='Chemical PU1 Gas'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='chem_pu1_oven',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chem_pu1_oven', to='cheminventory.Chemical', verbose_name='Chemical PU1 Oven'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='chem_pu2_gas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chem_pu2_gas', to='cheminventory.Chemical', verbose_name='Chemical PU2 Gas'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='chem_pu2_oven',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chem_pu2_oven', to='cheminventory.Chemical', verbose_name='Chemical PU2 Oven'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='cluster_size_distribution',
            field=models.FileField(blank=True, null=True, upload_to='clustof/clusterSizeDistribution/'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='data_filename',
            field=models.CharField(default='D:\\Data\\', max_length=1500, verbose_name='Filename'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='deflector_1',
            field=models.FloatField(verbose_name='Deflector oben/unten'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='deflector_2',
            field=models.FloatField(verbose_name='Deflector links/rechts'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='electron_energy_set',
            field=models.FloatField(blank=True, null=True, verbose_name='Electron Energy set on Power Supply (for MS)'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='evaluation_file',
            field=models.FileField(blank=True, default='', upload_to='clustof/evaluations/'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='is_inlet_gas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='is_inlet_gas', to='cheminventory.Chemical', verbose_name='Ion Source Inlet Gas'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='laser_power_file',
            field=models.FileField(blank=True, upload_to='clustof/powerfiles/', verbose_name='Laser Power Measurement File'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='lis_deflector_y',
            field=models.FloatField(blank=True, null=True, verbose_name='Deflector Y'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='lis_deflector_z',
            field=models.FloatField(blank=True, null=True, verbose_name='Deflector Z'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='lis_electron_energy',
            field=models.FloatField(blank=True, null=True, verbose_name='Electron energy'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='lis_filament_current',
            field=models.FloatField(blank=True, null=True, verbose_name='Filament current'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='lis_ion_block',
            field=models.FloatField(blank=True, null=True, verbose_name='Ion block'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='lis_trap_current',
            field=models.FloatField(blank=True, null=True, verbose_name='Trap current'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='polarity',
            field=models.CharField(choices=[('NEG', 'Negative'), ('POS', 'Positive'), ('OLD', 'Unknown (Old File)')], default='NEG', max_length=3),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='pressure_cs',
            field=models.FloatField(default=4e-05, verbose_name='Pressure CS'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='pressure_ion',
            field=models.FloatField(default=2e-08, verbose_name='Pressure ION'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='pressure_pu1',
            field=models.FloatField(default=3e-06, verbose_name='Pressure PU1'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='pressure_pu2',
            field=models.FloatField(default=1e-06, verbose_name='Pressure PU2'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='pressure_tof',
            field=models.FloatField(default=3e-07, verbose_name='Pressure TOF'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='real_electron_energy',
            field=models.FloatField(blank=True, null=True, verbose_name='Real Electron Energy (for MS)'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='scantype',
            field=models.CharField(choices=[('ES', 'Energyscan'), ('MS', 'Mass Spectrum'), ('TS', 'Temperature-Scan'), ('PS', 'Pressure-Scan'), ('LS', 'Laser-Scan'), ('OLD', 'Unknown (Old File)')], default='MS', max_length=20),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='stag_pressure_he',
            field=models.FloatField(default=25, verbose_name='He Stagnation Pressure'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='substance',
            field=models.TextField(max_length=1500, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='temperature_he',
            field=models.FloatField(default=9.0, verbose_name='He Temp'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='tof_settings_file',
            field=models.CharField(max_length=1500, verbose_name='TOF Settings File'),
        ),
    ]