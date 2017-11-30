# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-30 14:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rateMyCourse', '0012_merge_20171108_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discuss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000)),
                ('newmsg', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newmsg', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parentcomment',
        ),
        migrations.AddField(
            model_name='support',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rateMyCourse.Comment'),
        ),
        migrations.AddField(
            model_name='support',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rateMyCourse.User'),
        ),
        migrations.AddField(
            model_name='discuss',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rateMyCourse.Comment'),
        ),
        migrations.AddField(
            model_name='discuss',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rateMyCourse.User'),
        ),
    ]