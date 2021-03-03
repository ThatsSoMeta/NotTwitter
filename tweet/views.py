from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tweet
from .forms import TweetForm

# Create your views here.


def homepage_view(request):
    tweets = Tweet.objects.all().order_by('-id')
    return render(request, 'index.html', {'tweets': tweets})


@login_required
def tweet_view(request):
    form = TweetForm()
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Tweet.objects.create(
                author=request.user,
                text=data['text']
            )
            return redirect('/')
    return render(request, 'generic_form.html', {'form': form})
