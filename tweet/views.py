from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Tweet
from .forms import TweetForm
from notification.models import Notification
from twitteruser.models import TwitterUser
import re

# Create your views here.


def homepage_view(request):
    tweets = Tweet.objects.all().order_by('-id')
    notifications = 0
    if request.user:
        notifications = Notification.objects.filter(
            recipient=request.user, read=False
        ).count
    return render(
        request,
        'homepage.html',
        {'tweets': tweets, 'notifications': notifications}
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
    print(request)
    return redirect('/')


@login_required
def unlike_tweet(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    tweet.likes.remove(request.user)
    tweet.save()
    return redirect('/')


def tweet_detail_view(request, id):
    tweet = Tweet.objects.get(id=id)
    replies = Tweet.objects.filter(replying_to=tweet)
    form = TweetForm({'text': f'@{tweet.author} '})
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            text = data['text']
            new_tweet = Tweet.objects.create(
                author=request.user,
                text=text,
                replying_to=tweet
            )
            tweet.replies.add(new_tweet)
            tweet.save()
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
        form = TweetForm({'text': f'@{tweet.author} '})
        return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    return render(
        request,
        'tweet_details.html',
        {
            'tweet': tweet,
            'replies': replies,
            'form': form
        }
    )
