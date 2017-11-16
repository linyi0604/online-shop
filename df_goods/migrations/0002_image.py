# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('img_url', models.ImageField(verbose_name='详情图片', upload_to='Goods')),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='所属商品')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
    ]
