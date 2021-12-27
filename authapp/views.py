from django.contrib import auth
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, CreateView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileForm, ProfileForm
from authapp.models import ShopUser, ShopUserProfile
from basketapp.models import Basket
from django.conf import settings


class UserLoginView(LoginView):
    template_name = 'authapp/login.html'
    form_class = ShopUserLoginForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Авторизация'
        return context_data


class UserLogoutView(LogoutView):
    template_name = 'mainapp/index.html'


class Multiple(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Multiple, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user', )

    def save(self, commit=True):
        obj = super(Multiple, self).save(commit=False)
        obj.user = self.user
        if commit:
            return obj.save()
        else:
            return obj


class UserProfileView(UpdateView, Multiple):
    model = ShopUser
    template_name = 'authapp/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('authapp:profile')
    # fields = ('username', 'email', 'first_name', 'about_me')

    def save(self, **kwargs):
        data = super(UserProfileView, self).save(commit=False)
        return data.save()

    def get_success_url(self):
        return reverse('authapp:profile', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('pk')
        user_item = get_object_or_404(ShopUser, pk=user_id)
        context_data['title'] = 'Профиль'
        context_data['basket_list'] = Basket.objects.filter(user=user_item)
        return context_data


class UserRegistrationView(CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('authapp:login')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Регистрация'
        return context_data

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if form.is_valid():
            user = form.save()
            send_verify_mail(user)
        return super().form_valid(form)


def verify(request, email, activation_key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.activation_key_expired = None
            user.save()
            # auth.login(request, user)
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'authapp/verify.html')


def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    subject = 'Account verify'

    message = f'{settings.BASE_URL}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


# def register(request):
#     if request.method == 'POST':
#         register_form = ShopUserRegisterForm(data=request.POST)
#         if register_form.is_valid():
#             user = register_form.save()
#             send_verify_mail(user)
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

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
