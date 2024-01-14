from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, default='vanessa')
    last_name = models.CharField(max_length=100, default='marin')
    email = models.EmailField(unique=True, default="vanessa.vtm@gmail.com")
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, default="password")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Add related_name to resolve clashes
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True,
                                    help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True,
                                              help_text='Specific permissions for this user.')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
