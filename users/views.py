from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib import messages
# Create your views here.

from users.forms import UserLoginForm, UserRegistrationFrom, UserProfileForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()

    context = {'title': "Login", 'form': form}

    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationFrom(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались")
            return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationFrom()

    context = {'title': "Registration", 'form': form}

    return render(request, 'users/register.html', context)


def profile(request):
    if request.method == 'POST':
        # instance=request.user - говорит о том, что form.save сделает не
        # добавление пользователя, а обновление текущего пользователя (который сидит в профиле)
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {'title': 'Профиль', 'form': form}

    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))