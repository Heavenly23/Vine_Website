# Generated by Django 2.2.9 on 2020-01-26 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vine', '0002_auto_20200121_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='vine',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vine',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
