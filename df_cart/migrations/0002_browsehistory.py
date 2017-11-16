# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0003_auto_20170925_2124'),
        ('df_user', '0002_address'),
        ('df_cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrowseHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('goods', models.ForeignKey(verbose_name='商品', to='df_goods.Goods')),
                ('passport', models.ForeignKey(verbose_name='用户', to='df_user.PassPort')),
            ],
            options={
                'db_table': 's_browse_history',
            },
        ),
    ]
