# Generated by Django 3.1.6 on 2021-02-08 20:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210208_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 8, 22, 41, 11, 669609)),
        ),
        migrations.AlterField(
            model_name='student',
            name='Achievements',
            field=models.CharField(max_length=2500, null=True),
        ),
    ]
