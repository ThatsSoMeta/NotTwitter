from django.db import models
from twitteruser.models import TwitterUser
from tweet.models import Tweet

# Create your models here.


class Notification(models.Model):
    NEW = 'new'
    READ = 'read'
    DM = 'direct message'
    MENTION = 'mention'
    STATUS_CHOICES = [
        (True, READ), (False, NEW)
    ]
    TYPEOF_CHOICES = [
        DM, MENTION
    ]
    read = models.BooleanField(
        choices=STATUS_CHOICES,
        default=False
    )
    typeof = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=MENTION
    )
    sender = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        related_name='sender'
    )
    recipient = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        related_name='recipient'
    )
    reference = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        related_name='reference'
    )
