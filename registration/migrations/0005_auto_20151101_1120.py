# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_auto_20151029_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='widgetsubmission',
            name='widget_choice',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='widgetsubmission',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 11, 20, 8, 173143), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='widgetsubmission',
            name='updated_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 1, 11, 20, 8, 173174), auto_now=True),
            preserve_default=True,
        ),
    ]
