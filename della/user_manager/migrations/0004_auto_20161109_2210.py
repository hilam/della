# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-09 16:40
from __future__ import unicode_literals

import della.user_manager.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0003_userprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='/Users/avi/Documents/code/della/della/static/img/avatar.png', upload_to=della.user_manager.models.avatar_file_name),
        ),
    ]