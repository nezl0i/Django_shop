from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    context = {
        'title': 'Авторизация',
        'window_title': 'Вход в систему',
        'login_form': login_form
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit(request):
    return None


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(data=request.POST)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('authapp:login'))
    else:
        print('no')
        register_form = ShopUserRegisterForm()

    context = {
        'title': 'Регистрация',
        'window_title': 'Регистрация пользователя',
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', context)

# def register(request):
#     if request.method == 'POST':
#         register_form = ShopUserRegisterForm(data=request.POST)
#         if register_form.is_valid():
#             register_form.save()
#             messages.success(request, 'Вы успешно зарегистрировались!')
#             return HttpResponseRedirect(reverse('authapp:login'))
#     else:
#         register_form = ShopUserRegisterForm()
#     context = {'title': 'GeekShop - Регистрация', 'register_form': register_form}
#     return render(request, 'authapp/register.html', context)
