from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey


class UserFollows(models.Model):
    # Your UserFollows model definition goes here
    user = ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')


    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)


class User(AbstractUser):
    profile_picture = models.ImageField(default='default_profile.png', upload_to='profile_pictures/')
    followed = models.ManyToManyField(settings.AUTH_USER_MODEL, through=UserFollows)
