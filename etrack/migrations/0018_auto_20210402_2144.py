# Generated by Django 3.1.7 on 2021-04-02 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etrack', '0017_auto_20210402_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='express',
            name='packet_state',
            field=models.CharField(blank=True, default='未发送', max_length=20, verbose_name='快递单号'),
        ),
    ]
