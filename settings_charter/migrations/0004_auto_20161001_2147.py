# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings_charter', '0003_auto_20151208_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charterclubsettings',
            name='default_member_meals_per_semester',
            field=models.PositiveIntegerField(default=4, verbose_name=b'default number of guest meals for new member account'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='charterclubsettings',
            name='default_sophomore_meal_per_month',
            field=models.PositiveIntegerField(default=2, verbose_name=b'sophomore meal cap per month'),
            preserve_default=True,
        ),
    ]
