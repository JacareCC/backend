# Generated by Django 4.2.7 on 2023-12-06 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_alter_registrationrequests_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='qr_code_link',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]