# Generated by Django 3.2.5 on 2022-02-23 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default='2022-02-23'),
        ),
    ]