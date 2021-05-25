# Generated by Django 3.2.3 on 2021-05-25 16:45

import ckeditor.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('surftof', '0005_auto_20201020_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('short_description', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='surftof/journalimage/')),
                ('file', models.FileField(blank=True, null=True, upload_to='surftof/journalFiles/')),
                ('comment', ckeditor.fields.RichTextField(blank=True)),
            ],
        ),
    ]
