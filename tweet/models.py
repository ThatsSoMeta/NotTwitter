from django.db import models
from twitteruser.models import TwitterUser

# Create your models here.


class Tweet(models.Model):
    author = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=280)
    likes = models.ManyToManyField(
        TwitterUser, blank=True, related_name='likes'
    )
