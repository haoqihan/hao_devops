# Generated by Django 2.2 on 2020-03-26 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanhosts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='browseinfo',
            name='useragent',
            field=models.CharField(default='', max_length=256, null=True, verbose_name='用户浏览器的agent信息'),
        ),
    ]
