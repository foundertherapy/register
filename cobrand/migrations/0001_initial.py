# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CobrandCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('company_name', models.CharField(unique=True, max_length=100, db_index=True)),
                ('contact_email', models.EmailField(max_length=75)),
                ('contact_name', models.CharField(max_length=200)),
                ('uuid', shortuuidfield.fields.ShortUUIDField(db_index=True, unique=True, max_length=22, editable=False, blank=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
