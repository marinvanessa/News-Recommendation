# Generated by Django 4.2.7 on 2024-01-13 05:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_userlikes_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='news',
            name='number_of_likes',
        ),
    ]
