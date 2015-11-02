# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_auto_20151101_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='widgetsubmission',
            name='widget_choice',
        ),
        migrations.AddField(
            model_name='widgetsubmission',
            name='home_page_url',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='widgetsubmission',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='widgetsubmission',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
