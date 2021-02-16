# Generated by Django 3.1.6 on 2021-02-08 22:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20210209_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='surat',
            name='numberofayat',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='absence',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 9, 0, 58, 11, 921360)),
        ),
    ]
