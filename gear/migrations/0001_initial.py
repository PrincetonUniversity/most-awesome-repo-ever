# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GearItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('image_url', models.URLField()),
                ('sizes', models.CharField(default=b'', help_text=b'use abbreviations and separate with spaces (ex: xs s m l xl)', max_length=100, blank=True)),
                ('custom_text', models.IntegerField(default=0, help_text=b'max number of characters (0 if no custom text allowed)', blank=True)),
            ],
            options={
                'ordering': ('name', 'description'),
            },
            bases=(models.Model,),
        ),
    ]
