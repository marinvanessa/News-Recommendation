# Generated by Django 4.2.7 on 2023-11-25 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20231125_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='rating',
            field=models.IntegerField(default=1, max_length=100),
        ),
    ]