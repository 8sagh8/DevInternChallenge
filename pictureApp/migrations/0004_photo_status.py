# Generated by Django 3.1.4 on 2021-05-06 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pictureApp', '0003_auto_20210505_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
