# Generated by Django 4.2.7 on 2023-11-24 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jacare', '0005_points_tier_tierreward_user_visited_history_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerreviews',
            name='data',
            field=models.JSONField(default=dict),
        ),
    ]