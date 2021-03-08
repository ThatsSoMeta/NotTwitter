from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class TwitterUser(AbstractUser):
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='is_following'
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='is_followed_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    photo_url = models.URLField(
        blank=True,
        default='https://cdn3.iconfinder.com/data/icons/galaxy-open-line-gradient-i/200/contacts-512.png'
    )

    def __str__(self):
        return self.username
