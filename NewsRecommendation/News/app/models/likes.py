from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .user import CustomUser
from .news import News

from django.core.validators import MaxValueValidator, MinValueValidator

class UserLikes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])


