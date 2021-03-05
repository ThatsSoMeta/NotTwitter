from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.


@login_required
def notification_view(request):
    read = Notification.objects.filter(
        recipient=request.user, read=True
    ).order_by('-id')
    unread = Notification.objects.filter(
        recipient=request.user, read=False
    ).order_by('-id')
    for note in unread:
        note.read = True
        note.save()
    return render(
        request,
        'notifications.html',
        {'unread': unread, 'read': read}
    )


@login_required
def read_notification_view(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return redirect('/notifications/')
