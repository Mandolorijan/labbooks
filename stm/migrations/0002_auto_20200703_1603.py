# Generated by Django 3.0.8 on 2020-07-03 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stm', '0001_squashed_0006_auto_20180515_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='measurement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stm.Measurement'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stm.Sample'),
        ),
    ]