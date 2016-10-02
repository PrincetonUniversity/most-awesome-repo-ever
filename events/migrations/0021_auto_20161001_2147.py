# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20151208_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 10, 2, 1, 47, 55, 741284, tzinfo=utc), verbose_name=b'Date of Event'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='junior_signup_start',
            field=models.DateField(default=datetime.datetime(2016, 10, 2, 1, 47, 55, 741284, tzinfo=utc), blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='prospective_signup_start',
            field=models.DateField(default=datetime.datetime(2016, 10, 2, 1, 47, 55, 741284, tzinfo=utc), blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='senior_signup_start',
            field=models.DateField(default=datetime.datetime(2016, 10, 2, 1, 47, 55, 741284, tzinfo=utc), blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='signup_end_time',
            field=models.DateField(default=datetime.datetime(2016, 10, 2, 1, 47, 55, 741284, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='sophomore_signup_start',
            field=models.DateField(default=datetime.datetime(2016, 10, 2, 1, 47, 55, 741284, tzinfo=utc), blank=True),
            preserve_default=True,
        ),
    ]
