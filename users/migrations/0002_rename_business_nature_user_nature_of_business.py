# Generated by Django 3.2.4 on 2021-07-17 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='business_nature',
            new_name='nature_of_business',
        ),
    ]