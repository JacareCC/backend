# Generated by Django 4.2.7 on 2023-12-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0013_merge_20231221_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='qr_code_link',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]