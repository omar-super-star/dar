# Generated by Django 3.1.6 on 2021-02-12 00:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_auto_20210211_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='paid',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='absence',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 12, 0, 37, 32, 666443)),
        ),
    ]