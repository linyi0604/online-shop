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
            name='OrderBasic',
            fields=[
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('order_id', models.CharField(max_length=32, verbose_name='订单编号', primary_key=True, serialize=False)),
                ('total_count', models.IntegerField(default=0, verbose_name='商品总数')),
                ('total_exprice', models.DecimalField(verbose_name='商品总价', decimal_places=2, max_digits=10)),
                ('transit_price', models.DecimalField(verbose_name='运费', decimal_places=2, max_digits=10)),
                ('pay_method', models.IntegerField(default=1, verbose_name='支付方式')),
                ('order_status', models.IntegerField(default=1, verbose_name='订单状态')),
                ('addr', models.ForeignKey(verbose_name='收货地址', to='df_user.Address')),
                ('passport', models.ForeignKey(verbose_name='所属账户', to='df_user.PassPort')),
            ],
            options={
                'db_table': 's_order_basic',
            },
        ),
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('goods_count', models.IntegerField(default=0, verbose_name='商品数目')),
                ('goods_price', models.DecimalField(verbose_name='商品价格', decimal_places=2, max_digits=10)),
                ('goods', models.ForeignKey(verbose_name='商品', to='df_goods.Goods')),
                ('order', models.ForeignKey(verbose_name='所属订单', to='df_order.OrderBasic')),
            ],
            options={
                'db_table': 's_order_detail',
            },
        ),
    ]
