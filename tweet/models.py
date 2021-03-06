from django.db import models
from twitteruser.models import TwitterUser

# Create your models here.


class Tweet(models.Model):
    author = models.ForeignKey(
        TwitterUser, on_delete=models.CASCADE, related_name='author'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(
        max_length=140,
    )
    likes = models.ManyToManyField(
        TwitterUser, blank=True, related_name='likes'
    )
    replying_to = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='reply',
        on_delete=models.CASCADE
    )
    replies = models.ManyToManyField(
        'self', blank=True,
        related_name='replies'
    )
