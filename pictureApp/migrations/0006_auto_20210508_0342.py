# Generated by Django 3.1.4 on 2021-05-08 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictureApp', '0005_photo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
