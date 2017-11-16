# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PassPort',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=20, verbose_name='账户名称')),
                ('password', models.CharField(max_length=40, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
            ],
            options={
                'db_table': 's_user_account',
            },
        ),
    ]
