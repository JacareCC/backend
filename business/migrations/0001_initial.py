# Generated by Django 4.2.7 on 2023-12-01 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('business_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_person', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=15)),
                ('status', models.CharField(default='pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_id', models.TextField()),
                ('business_name', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('phone_number', models.CharField(max_length=15, null=True)),
                ('contact_person', models.CharField(max_length=200, null=True)),
                ('retaurant_level', models.IntegerField(null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('claimed', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TierReward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reward_level', models.CharField()),
                ('reward_description', models.TextField()),
                ('points_required', models.IntegerField()),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.restaurant')),
            ],
        ),
    ]
