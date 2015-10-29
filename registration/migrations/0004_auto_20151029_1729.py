# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20151029_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widgetsubmission',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 29, 17, 29, 27, 875806), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='widgetsubmission',
            name='updated_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 29, 17, 29, 27, 875846), auto_now=True),
            preserve_default=True,
        ),
    ]
