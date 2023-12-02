from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=100, default='vanessa')
    last_name = models.CharField(max_length=100, default='marin')
    email = models.CharField(max_length=100, default='vaness@gmail.com')
    username = models.CharField(max_length=100, default='xxvanexx')
    password = models.CharField(max_length=100, default="password")

