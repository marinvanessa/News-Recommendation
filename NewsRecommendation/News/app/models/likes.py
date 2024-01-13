from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .user import User
from .news import News


class UserLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])

