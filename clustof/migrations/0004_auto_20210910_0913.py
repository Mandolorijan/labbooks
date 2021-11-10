# Generated by Django 3.2.7 on 2021-09-10 07:13

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clustof', '0003_measurement_pressure_pu3'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CurrentSetting',
        ),
        migrations.AlterModelOptions(
            name='journalentry',
            options={},
        ),
        migrations.RemoveField(
            model_name='journalentry',
            name='written_notes',
        ),
        migrations.AddField(
            model_name='journalentry',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='journal/journalImage/'),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='journal/journalImage/'),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='journal/journalImage/'),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='journal/journalImage/'),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='image5',
            field=models.ImageField(blank=True, null=True, upload_to='journal/journalImage/'),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='measurement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='clustof.measurement'),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='title',
            field=models.CharField(default=' ', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='journal/journalFiles/', verbose_name='File which can be downloaded'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='comment',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='clustof.operator'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]