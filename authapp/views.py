from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, CreateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from basketapp.models import Basket


class UserLoginView(LoginView):
    template_name = 'authapp/login.html'
    form_class = ShopUserLoginForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Авторизация'
        return context_data



# def login(request):
#     login_form = ShopUserLoginForm(data=request.POST)
#     next_url = request.GET.get('next', '')
#     if request.method == 'POST' and login_form.is_valid():
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = auth.authenticate(username=username, password=password)
#         if user and user.is_active:
#             auth.login(request, user)
#             if 'next' in request.POST:
#                 return HttpResponseRedirect(request.POST['next'])
#             return HttpResponseRedirect(reverse('index'))
#
#     context = {
#         'title': 'Авторизация',
#         'window_title': 'Вход в систему',
#         'form': login_form,
#         'next': next_url
#     }
#     return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class UserProfileView(UpdateView):
    model = ShopUser
    template_name = 'authapp/profile.html'
    form_class = ShopUserEditForm
    success_url = reverse_lazy('authapp:login')

    def get_success_url(self):
        return reverse('authapp:login', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('pk')
        user_item = get_object_or_404(ShopUser, pk=user_id)
        context_data['title'] = 'Профиль'
        context_data['basket_list'] = Basket.objects.filter(user=user_item)
        print(context_data['basket_list'])
        return context_data


# def edit(request):
#     if request.method == 'POST':
#         edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('authapp:profile'))
#     else:
#         edit_form = ShopUserEditForm(instance=request.user)
#
#     context = {
#         'title': 'Редактирование',
#         'window_title': 'Редактирование профиля',
#         'form': edit_form
#     }
#
#     return render(request, 'authapp/profile.html', context)


class UserRegistrationView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('authapp:login')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Регистрация'
        return context_data

# def register(request):
#     if request.method == 'POST':
#         register_form = ShopUserRegisterForm(data=request.POST)
#         if register_form.is_valid():
#             register_form.save()
#             return HttpResponseRedirect(reverse('authapp:login'))
#     else:
#         register_form = ShopUserRegisterForm()
#
#     context = {
#         'title': 'Регистрация',
#         'window_title': 'Регистрация пользователя',
#         'form': register_form
#     }
#
#     return render(request, 'authapp/register.html', context)
