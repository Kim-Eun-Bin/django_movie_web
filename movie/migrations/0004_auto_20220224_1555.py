# Generated by Django 3.2.5 on 2022-02-24 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_auto_20220223_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='movie_id',
            field=models.TextField(),
        ),
        migrations.DeleteModel(
            name='Movie_info',
        ),
    ]
