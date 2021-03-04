from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tweet
from .forms import TweetForm
from notification.models import Notification
from twitteruser.models import TwitterUser
import re

# Create your views here.


def homepage_view(request):
    tweets = Tweet.objects.all().order_by('-id')
    # if request.user:
    #     notifications = Notification.objects.filter(recipient=request.user)
    # else:
    #     notifications = []
    return render(
        request,
        'index.html',
        {'tweets': tweets}
    )


@login_required
def tweet_view(request):
    form = TweetForm()
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            text = data['text']
            tweet = Tweet.objects.create(
                author=request.user,
                text=text
            )
            if '@' in text:
                mentions = re.findall(r"@(\w+)", text)
                print(mentions)
                for username in mentions:
                    user = TwitterUser.objects.filter(
                        username__iexact=username
                    )
                    if user:
                        notice = Notification.objects.create(
                            typeof=Notification.MENTION,
                            sender=request.user,
                            recipient=user.first(),
                            reference=tweet
                        )
                        print(notice)
            return redirect('/')
    return render(request, 'generic_form.html', {'form': form})


@login_required
def like_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    tweet.likes.add(request.user)
    tweet.save()
    return redirect('/')


@login_required
def unlike_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    tweet.likes.remove(request.user)
    tweet.save()
    return redirect('/')
