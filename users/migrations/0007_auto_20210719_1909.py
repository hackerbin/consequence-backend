# Generated by Django 3.2.4 on 2021-07-19 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210719_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='natureofbusiness',
            name='impact_per_member',
            field=models.FloatField(default=78.46),
        ),
        migrations.AlterField(
            model_name='natureofbusiness',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
