# Generated by Django 4.2.7 on 2023-11-25 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_news_rating_news_like_news_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='number_of_likes',
            field=models.IntegerField(default=0),
        ),
    ]
