# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_auto_20151102_1043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='widgetsubmission',
            old_name='company_source',
            new_name='widget_id',
        ),
    ]
