# Generated by Django 3.2.4 on 2021-07-23 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truelayer', '0012_auto_20210723_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classification',
            old_name='title',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='classification',
            old_name='subtitle',
            new_name='subcategory',
        ),
        migrations.AlterField(
            model_name='classification',
            name='co2e_factor',
            field=models.FloatField(default=203.76),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='co2e_factor',
            field=models.FloatField(default=235.63),
        ),
        migrations.AlterUniqueTogether(
            name='classification',
            unique_together={('category', 'subcategory')},
        ),
    ]
