# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-22 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organlization', '0003_auto_20180321_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='教师头像'),
        ),
    ]
