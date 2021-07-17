# Generated by Django 3.2.4 on 2021-07-13 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=64, unique=True)),
                ('account_type', models.CharField(max_length=64)),
                ('display_name', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=10)),
                ('account_number', models.JSONField()),
                ('provider', models.JSONField()),
                ('update_timestamp', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=64, unique=True)),
                ('card_network', models.CharField(max_length=64)),
                ('card_type', models.CharField(max_length=64)),
                ('currency', models.CharField(max_length=10)),
                ('display_name', models.CharField(max_length=255)),
                ('partial_card_number', models.CharField(max_length=64)),
                ('name_on_card', models.CharField(max_length=255)),
                ('provider', models.JSONField()),
                ('update_timestamp', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('co2e_factor', models.FloatField(default=222.69)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('co2e_factor', models.FloatField(default=38.7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('bank', 'Bank'), ('card', 'Card')], max_length=10)),
                ('account_id', models.CharField(max_length=64)),
                ('timestamp', models.DateTimeField()),
                ('description', models.CharField(max_length=255)),
                ('transaction_type', models.CharField(max_length=64)),
                ('transaction_category', models.CharField(max_length=64)),
                ('amount', models.FloatField()),
                ('currency', models.CharField(max_length=10)),
                ('transaction_id', models.CharField(max_length=64)),
                ('running_balance', models.JSONField()),
                ('meta', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('merchant_name', models.ManyToManyField(related_name='transactions', to='truelayer.Merchant')),
                ('transaction_classification', models.ManyToManyField(related_name='transactions', to='truelayer.Classification')),
            ],
        ),
    ]