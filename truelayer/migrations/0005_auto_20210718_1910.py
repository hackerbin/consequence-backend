# Generated by Django 3.2.4 on 2021-07-18 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truelayer', '0004_auto_20210717_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classification',
            name='co2e_factor',
            field=models.FloatField(default=253.03),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='co2e_factor',
            field=models.FloatField(default=177.31),
        ),
    ]
