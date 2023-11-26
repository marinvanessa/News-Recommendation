# Generated by Django 4.2.7 on 2023-11-25 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_user_las_name_user_email_user_last_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='news', max_length=100)),
                ('description', models.CharField(default='description', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='news',
            field=models.ManyToManyField(to='app.news'),
        ),
    ]
