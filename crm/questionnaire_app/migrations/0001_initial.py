# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 00:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
            ],
            options={
                'verbose_name_plural': '管理员表',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('val', models.IntegerField(blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': '答案表',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='选项标题')),
                ('score', models.IntegerField(verbose_name='选项分数')),
            ],
            options={
                'verbose_name_plural': '问题选项表',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(blank=True, max_length=16, verbose_name='部门名称')),
            ],
            options={
                'verbose_name_plural': '部门表',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire_app.Department', verbose_name='部门')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question_type', models.IntegerField(choices=[(1, '单选'), (2, '多选'), (3, '打分'), (4, '建议')], verbose_name='问题类型')),
                ('content', models.CharField(max_length=256, verbose_name='问题内容')),
            ],
            options={
                'verbose_name_plural': '问题表',
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='问卷标题')),
                ('description', models.CharField(max_length=512, verbose_name='问卷描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire_app.Admin', verbose_name='创建人')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire_app.Department', verbose_name='接受调查的部门')),
            ],
            options={
                'verbose_name_plural': '问卷表',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire_app.Questionnaire', verbose_name='所属问卷'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire_app.Question', verbose_name='所属问题'),
        ),
        migrations.AddField(
            model_name='answer',
            name='choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='questionnaire_app.Choice'),
        ),
        migrations.AddField(
            model_name='answer',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire_app.Employee', verbose_name='回答员工'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire_app.Question', verbose_name='对应问题'),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('employee', 'question')]),
        ),
    ]