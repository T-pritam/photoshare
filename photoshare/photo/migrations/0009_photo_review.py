# Generated by Django 4.0.4 on 2022-08-10 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0008_photo_uploaddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='review',
            field=models.IntegerField(default=0),
        ),
    ]