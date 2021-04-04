# Generated by Django 3.1.7 on 2021-04-04 01:23

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etrack', '0019_auto_20210402_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='express',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='寄件登录时间'),
        ),
        migrations.AlterField(
            model_name='express',
            name='recipient_photo',
            field=models.ImageField(blank=True, storage=django.core.files.storage.FileSystemStorage(location='/media/photos'), upload_to='', verbose_name='收件人身份证照片上传'),
        ),
    ]
