# Generated by Django 3.1.6 on 2021-02-10 19:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20210210_0516'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='homeworkdegree',
            field=models.CharField(blank=True, choices=[('ممتاز', 'ممتاز'), ('جيد جدا', 'جيد جدا'), ('جيد', 'جيد'), ('مقبول', 'مقبول'), ('اعادة', 'اعادة')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='absence',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 10, 19, 31, 6, 504550)),
        ),
    ]