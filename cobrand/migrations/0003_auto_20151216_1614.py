# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cobrand', '0002_auto_20151109_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cobrandcompany',
            name='contact_email',
            field=models.EmailField(max_length=254),
        ),
    ]
