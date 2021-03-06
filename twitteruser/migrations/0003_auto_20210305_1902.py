# Generated by Django 3.1.7 on 2021-03-05 19:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitteruser', '0002_remove_twitteruser_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='_twitteruser_followers_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='twitteruser',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='_twitteruser_following_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
