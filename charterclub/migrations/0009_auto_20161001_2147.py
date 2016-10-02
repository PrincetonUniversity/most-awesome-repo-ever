# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import charterclub.models


class Migration(migrations.Migration):

    dependencies = [
        ('charterclub', '0008_member_guest_meals'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='guest_meals',
            field=models.IntegerField(default=charterclub.models.get_default_guest_meals, verbose_name=b'number of guest meals this member has'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='house_account',
            field=models.DecimalField(default=charterclub.models.get_default_house_account, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(validators=[charterclub.models.validate_image], upload_to=b'member_images/', blank=True, help_text=b'(optional)', null=True),
            preserve_default=True,
        ),
    ]
