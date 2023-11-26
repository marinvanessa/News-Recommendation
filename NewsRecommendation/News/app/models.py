from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100, default='vanessa')
    last_name = models.CharField(max_length=100, default='marin')
    email = models.CharField(max_length=100, default='vaness@gmail.com')
    username = models.CharField(max_length=100, default='xxvanexx')


class News(models.Model):
    title = models.CharField(max_length=100, default='news')
    description = models.CharField(max_length=100, default='description')
    link = models.CharField(max_length=100, default='link')
    number_of_likes = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, through='UserLikes', related_name='liked_news')


class UserLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)
