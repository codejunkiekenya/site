# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-28 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='review_image',
        ),
        migrations.AddField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d'),
        ),
        migrations.DeleteModel(
            name='Images',
        ),
    ]
