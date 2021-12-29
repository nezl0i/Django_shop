import hashlib
from random import random
from datetime import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import ModelForm

from authapp.models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = ShopUser
        fields = ('username', 'password')
    # class Meta:
    #     model = ShopUser
    #     fields = ('username', 'password',)
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control py-4'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'last_name', 'first_name', 'email', 'age', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        salt = hashlib.sha1(str(random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.activation_key_expired = datetime.now()
        # user.save()
        return user

    def clean_age(self):
        data_age = self.cleaned_data['age']
        if data_age < 18:
            raise forms.ValidationError('Ваш возраст слишком маленький.')
        return data_age


class CombinedForm(forms.Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        super(CombinedForm, self).__init__(*args, **kwargs)
        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super(CombinedForm, self).clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data


class ShopUserEditForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = ShopUser
        fields = ('username', 'email', 'age', 'first_name', 'last_name', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
            if field_name == 'password':
                field.widget = forms.HiddenInput()
    #
    # def clean_age(self):
    #     data_age = self.cleaned_data['age']
    #     if data_age < 18:
    #         raise forms.ValidationError('Ваш возраст слишком маленький.')
    #     return data_age

    # username = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    # email = forms.CharField(widget=forms.EmailInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    # first_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Введите имя'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}))
    # avatar = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control py-4', }),
    #                          required=False, label=u'Аватар')
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))
    #
    # class Meta:
    #     model = ShopUser
    #     fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'password1', 'password2')


class ShopUserProfileForm(ModelForm):

    class Meta:
        model = ShopUserProfile
        fields = ('tagline', 'about_me', 'gender')
        form_class = ShopUserEditForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class ProfileForm(CombinedForm):
    form_classes = [ShopUserEditForm, ShopUserProfileForm]
