# Generated by Django 4.2.7 on 2023-12-07 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jacare', '0011_customerreviews_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerreviews',
            name='isHidden',
            field=models.BooleanField(default=False),
        ),
    ]
