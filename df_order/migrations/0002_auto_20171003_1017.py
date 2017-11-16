# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderbasic',
            old_name='total_exprice',
            new_name='total_price',
        ),
        migrations.AlterField(
            model_name='orderbasic',
            name='order_id',
            field=models.CharField(max_length=64, verbose_name='订单编号', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='orderbasic',
            name='passport',
            field=models.ForeignKey(verbose_name='所属用户', to='df_user.PassPort'),
        ),
        migrations.AlterField(
            model_name='orderbasic',
            name='total_count',
            field=models.IntegerField(verbose_name='商品总数', default=1),
        ),
    ]
