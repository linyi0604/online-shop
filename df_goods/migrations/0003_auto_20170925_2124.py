# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img_url',
            field=models.ImageField(upload_to='goods', verbose_name='详情图片'),
        ),
    ]
