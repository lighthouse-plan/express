# Generated by Django 3.1.7 on 2021-03-24 10:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_name', models.CharField(max_length=200, null=True, verbose_name='发件人姓名')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='')),
                ('sender_wechat_name', models.CharField(max_length=200, null=True, verbose_name='发件人微信名字')),
                ('sender_wechat_num', models.CharField(max_length=200, verbose_name='发件人微信号')),
                ('sender_phone_num', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message='请输入日本电话号码', regex='^\\?1?\\d{9,15}$')], verbose_name='发件人电话号码')),
                ('recipient_name', models.CharField(max_length=200, verbose_name='收件人姓名')),
                ('recipient_phone_num', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message='请输入日本电话号码', regex='^\\?1?\\d{9,15}$')], verbose_name='收件人手机号码')),
                ('recipient_country', models.CharField(default='中国', max_length=200, verbose_name='收件人国家')),
                ('recipient_province', models.CharField(max_length=200, verbose_name='收件人省')),
                ('recipient_city', models.CharField(max_length=200, verbose_name='收件人市')),
                ('recipient_district', models.CharField(max_length=200, verbose_name='收件人区（县）')),
                ('recipient_addr', models.CharField(max_length=200, verbose_name='收件人详细地址')),
                ('recipient_id', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='请输入正确的身份证号', regex='^[1-9]\\d{5}(18|19|20)\\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$')], verbose_name='收件人身份证号码')),
            ],
        ),
    ]
