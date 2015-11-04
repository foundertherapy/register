# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoBrandingRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('company_name', models.CharField(max_length=30)),
                ('company_logo', models.CharField(max_length=255, null=True, blank=True)),
                ('company_home_url', models.CharField(max_length=255, null=True, blank=True)),
                ('cobrand_id', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
