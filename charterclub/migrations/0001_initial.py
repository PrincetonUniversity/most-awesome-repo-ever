# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import charterclub.models


class Migration(migrations.Migration):

    dependencies = [
        ('kitchen', '0003_auto_20150904_0300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=40)),
                ('snippet', models.CharField(max_length=150, blank=True)),
                ('date_and_time', models.DateTimeField(blank=True)),
                ('end_time', models.DateTimeField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='charterclub.Person')),
                ('position', models.CharField(max_length=100, verbose_name=b"Staff's position/title")),
            ],
            options={
            },
            bases=('charterclub.person',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='charterclub.Person')),
                ('netid', models.CharField(max_length=100, verbose_name=b'Princeton Net ID', validators=[django.core.validators.RegexValidator(b'^[0-9a-zA-Z]*$', b'Only alphanumeric characters are allowed.')])),
                ('year', models.IntegerField(verbose_name=b'Graduation Year')),
            ],
            options={
            },
            bases=('charterclub.person',),
        ),
        migrations.CreateModel(
            name='Prospective',
            fields=[
                ('student_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='charterclub.Student')),
                ('events_attended', models.IntegerField(verbose_name=b'Number of events attended')),
                ('meals_attended', models.ManyToManyField(to='kitchen.Meal')),
            ],
            options={
            },
            bases=('charterclub.student',),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('student_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='charterclub.Student')),
                ('house_account', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('image', models.ImageField(blank=True, null=True, upload_to=b'member_images/', validators=[charterclub.models.validate_image])),
                ('allow_rsvp', models.BooleanField(default=True, verbose_name=b'Whether or not this member may attend events')),
            ],
            options={
            },
            bases=('charterclub.student',),
        ),
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('member_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='charterclub.Member')),
                ('position', models.CharField(max_length=100, verbose_name=b'Position/title')),
            ],
            options={
            },
            bases=('charterclub.member',),
        ),
    ]