from django.db import models
from ..models.user import User


class News(models.Model):
    title = models.CharField(max_length=100, default='news')
    description = models.CharField(max_length=150, default='description')
    link = models.CharField(max_length=100, default='link')
    number_of_likes = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, through='UserLikes', related_name='liked_news')
