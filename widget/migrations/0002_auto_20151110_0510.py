# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('widget', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WidgetHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('uuid', shortuuidfield.fields.ShortUUIDField(db_index=True, unique=True, max_length=22, editable=False, blank=True)),
                ('contact_email', models.EmailField(max_length=75)),
                ('contact_name', models.CharField(max_length=200)),
                ('host_url', models.URLField(max_length=255)),
            ],
            options={
                'verbose_name': 'Widget Host',
                'verbose_name_plural': 'Widget Hosts',
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='WidgetSubmission',
        ),
    ]
