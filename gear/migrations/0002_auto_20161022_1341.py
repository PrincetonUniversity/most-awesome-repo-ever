# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gear', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gearitem',
            name='custom_text',
        ),
        migrations.AddField(
            model_name='gearitem',
            name='inventory',
            field=models.IntegerField(default=0, help_text=b'Number of this item remaining'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gearitem',
            name='sizes',
            field=models.CharField(default=b'', help_text=b'Create a new item for each size option for this item', max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
