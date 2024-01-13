from django.db import models


class News(models.Model):
    title = models.CharField(max_length=100, default='news')
    description = models.CharField(max_length=150, default='description')
    link = models.CharField(max_length=100, default='link')
