# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cobrand', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cobrandcompany',
            options={'verbose_name': 'Cobrand Company', 'verbose_name_plural': 'Cobrand Companies'},
        ),
        migrations.AlterField(
            model_name='cobrandcompany',
            name='slug',
            field=models.SlugField(unique=True, editable=False),
            preserve_default=True,
        ),
    ]
