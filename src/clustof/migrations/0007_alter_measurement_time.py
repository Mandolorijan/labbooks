# Generated by Django 3.2.9 on 2021-11-10 15:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clustof', '0006_alter_journalentry_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]