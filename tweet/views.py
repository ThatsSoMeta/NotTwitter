from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Tweet
from .forms import TweetForm
from notification.models import Notification
from twitteruser.models import TwitterUser
import re

# Create your views here.


@login_required
def homepage_view(request):
    following = request.user.following.all()
    tweets = Tweet.objects.filter(
        Q(author__in=following) | Q(author=request.user)
    ).order_by('-created_at')
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
    notifications = Notification.objects.filter(
        recipient=request.user, read=False
    ).count
    return render(
        request,
        'generic_form.html',
        {'form': form, 'notifications': notifications}
    )


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
                        reference=new_tweet
                    )
                    print(notice)
        form = TweetForm({'text': f'@{tweet.author} '})
        return redirect(reverse('tweet', args=[tweet.id]))
    notifications = 0
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            recipient=request.user, read=False
        ).count
    if tweet.replying_to:
        return redirect(reverse('tweet', args=[tweet.replying_to.id]))
    return render(
        request,
        'tweet_details.html',
        {
            'tweet': tweet,
            'replies': replies,
            'form': form,
            'notifications': notifications,
        }
    )
