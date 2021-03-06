# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 10:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='邮箱')),
                ('username', models.CharField(max_length=16, unique=True, verbose_name='用户名')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='用户注册时间')),
                ('location', models.CharField(blank=True, max_length=10, verbose_name='城市')),
                ('profile', models.CharField(blank=True, max_length=140, verbose_name='个人简介')),
                ('avatar', models.CharField(blank=True, max_length=128, verbose_name='头像')),
                ('last_ip', models.GenericIPAddressField(default='0.0.0.0', verbose_name='上次访问IP')),
                ('email_verified', models.BooleanField(default=False, verbose_name='邮箱是否验证')),
                ('topic_num', models.IntegerField(default=0, verbose_name='帖子数')),
                ('comment_num', models.IntegerField(default=0, verbose_name='评论数')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailVerified',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=None, max_length=32, verbose_name='Email 验证 token')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='users.MyUser')),
            ],
        ),
        migrations.CreateModel(
            name='FindPass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=32)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.MyUser', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_followed', models.DateTimeField(default=django.utils.timezone.now)),
                ('from_friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_set', to='users.MyUser')),
                ('to_friend', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_friend_set', to='users.MyUser')),
            ],
        ),
    ]
