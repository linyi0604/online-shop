# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('is_delete', models.BooleanField(verbose_name='删除标记', default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('recipient_name', models.CharField(verbose_name='收件人', max_length=24)),
                ('recipient_addr', models.CharField(verbose_name='收件地址', max_length=256)),
                ('recipient_phone', models.CharField(verbose_name='联系电话', max_length=11)),
                ('zip_code', models.CharField(verbose_name='邮政编码', max_length=6)),
                ('is_default', models.BooleanField(verbose_name='是否默认', default=False)),
                ('passport', models.ForeignKey(verbose_name='所属账户', to='df_user.PassPort')),
            ],
            options={
                'db_table': 's_user_address',
            },
        ),
    ]
