from django.shortcuts import render
from .models import Tweet

# Create your views here.


def homepage_view(request):
    tweets = Tweet.objects.all()
    return render(request, 'index.html', {'tweets': tweets})