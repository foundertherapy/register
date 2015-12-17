# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('widget', '0004_auto_20151125_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widgethost',
            name='contact_email',
            field=models.EmailField(max_length=254),
        ),
    ]
