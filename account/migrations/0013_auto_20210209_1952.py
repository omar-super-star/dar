# Generated by Django 3.1.6 on 2021-02-09 17:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20210209_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 9, 19, 52, 52, 278781)),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='hour',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
