# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('widget', '0002_auto_20151110_0510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widgethost',
            name='host_url',
            field=models.URLField(unique=True, max_length=255),
            preserve_default=True,
        ),
    ]
