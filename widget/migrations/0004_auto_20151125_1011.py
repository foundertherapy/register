# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('widget', '0003_auto_20151110_0526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widgethost',
            name='host_url',
            field=models.CharField(unique=True, max_length=255, validators=[django.core.validators.URLValidator()]),
            preserve_default=True,
        ),
    ]
