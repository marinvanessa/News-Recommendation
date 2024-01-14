from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200, default='news')
    description = models.CharField(max_length=255, default='description')
    link = models.CharField(max_length=200, default='link')
