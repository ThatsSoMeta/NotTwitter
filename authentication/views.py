from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from twitteruser.forms import CreateUserForm, LoginForm

# Create your views here.


def register_view(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            username = data['username']
            password = data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    return render(
        request, 'register.html', {'form': form, 'header': "Register"}
    )


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    return render(
        request,
        'generic_form.html',
        {
            'form': form,
            'header': 'Login'
        }
    )


def logout_view(request):
    logout(request)
    return redirect('/')
