# Generated by Django 3.1.6 on 2021-02-09 15:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20210209_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='absence',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='student',
            name='degree',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='absence',
            name='day',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 9, 17, 47, 37, 687916)),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lecture_teacher', to='account.teacher'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='manager',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager_settings', to='account.manager'),
        ),
        migrations.AlterField(
            model_name='student',
            name='Achievements',
            field=models.CharField(blank=True, max_length=2500, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='aya',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_aya', to='account.aya'),
        ),
        migrations.AlterField(
            model_name='student',
            name='barcode',
            field=models.CharField(blank=True, max_length=2500, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_teacher', to='account.teacher'),
        ),
        migrations.AlterField(
            model_name='surat',
            name='numberofayat',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager_teacher', to='account.manager'),
        ),
    ]
