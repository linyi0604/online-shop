# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_address'),
        ('df_goods', '0003_auto_20170925_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('goods_count', models.IntegerField(verbose_name='商品数量')),
                ('goods', models.ForeignKey(verbose_name='商品', to='df_goods.Goods')),
                ('passport', models.ForeignKey(verbose_name='账户', to='df_user.PassPort')),
            ],
            options={
                'db_table': 's_cart',
            },
        ),
    ]
