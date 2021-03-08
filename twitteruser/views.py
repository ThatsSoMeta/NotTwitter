from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import TwitterUser
from notification.models import Notification
from tweet.models import Tweet


def user_detail_view(request, username):
    user = TwitterUser.objects.get(username=username)
    if request.method == 'POST':
        print(request.POST['url'])
        if user == request.user:
            print('This is the right user')
            user.photo_url = request.POST['url']
            user.save()
            return redirect(f'/users/{ user.username }')
    tweets = Tweet.objects.filter(author=user).order_by('-id')
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            recipient=request.user, read=False
        ).count
    else:
        notifications = 0
    return render(
        request,
        'user_detail.html',
        {
            'currentuser': user,
            'tweets': tweets,
            'notifications': notifications,
        }
    )


@login_required
def follow_user(request, username):
    currentuser = TwitterUser.objects.get(username=request.user.username)
    user = TwitterUser.objects.get(username=username)
    currentuser.following.add(user)
    currentuser.save()
    user.followers.add(currentuser)
    user.save()
    return redirect(f'/users/{user.username}')


@login_required
def unfollow_user(request, username):
    currentuser = TwitterUser.objects.get(username=request.user.username)
    user = TwitterUser.objects.get(username=username)
    currentuser.following.remove(user)
    currentuser.save()
    user.followers.remove(currentuser)
    user.save()
    return redirect(f'/users/{user.username}')


@login_required
def view_all_users(request):
    users = TwitterUser.objects.filter(
        ~Q(username=request.user.username)
    )
    return render(
        request,
        'user_list.html',
        {'users': users}
    )
