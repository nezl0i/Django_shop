from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


# Пользователи
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'title': 'Пользователи',
        'object_list': ShopUser.objects.all().order_by('-is_active'),
    }
    return render(request, 'adminapp/users_list.html', context)


# Создание пользователя
@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': 'Создание пользователя',
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)


# Редактирование пользователя
@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    selected_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        form = ShopUserAdminEditForm(request.POST, instance=selected_user, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:users'))
    else:
        form = ShopUserAdminEditForm(instance=selected_user)
    context = {
        'title': 'Редактирование пользователя',
        'form': form,
        'user': selected_user,
    }
    return render(request, 'adminapp/user_form.html', context)


# Удаление пользователя
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        current_user.is_active = False
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:users'))
    context = {
        'title': 'Удаление пользователя',
        'object': current_user
    }
    return render(request, 'adminapp/user_delete.html', context)


# Категории
@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'title': 'Категории товаров',
        'object_list': ProductCategory.objects.all()
    }

    return render(request, 'adminapp/categories_list.html', context)


# Создание категории
@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductCategoryForm()

    context = {
        'title': 'Создание категории',
        'form': form
    }
    return render(request, 'adminapp/category_form.html', context)


# Редактирование категории
@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category_item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductCategoryForm(instance=category_item)

    context = {
        'title': 'Изменение категории',
        'form': form
    }
    return render(request, 'adminapp/category_form.html', context)


# Удаление категории
@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        category_item.is_active = False
        category_item.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))
    context = {
        'title': 'Удаление категории',
        'object': category_item
    }
    return render(request, 'adminapp/category_delete.html', context)


# Продукты
@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'title': 'Товары',
        'object_list': Product.objects.filter(category__pk=pk)
    }

    return render(request, 'adminapp/products_list.html', context)


# Создание продукта
@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductEditForm()

    context = {
        'title': 'Создание товара',
        'form': form
    }
    return render(request, 'adminapp/product_form.html', context)


# Редактирование продукта
@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=product_item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:categories'))
    else:
        form = ProductEditForm(instance=product_item)

    context = {
        'title': 'Редактирование товара',
        'form': form
    }
    return render(request, 'adminapp/product_form.html', context)


# Удаление продукта
@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_item.is_active = False
        product_item.save()
        return HttpResponseRedirect(reverse('adminapp:categories'))
    context = {
        'title': 'Удаление товара',
        'object': product_item
    }
    return render(request, 'adminapp/product_delete.html', context)


# Просмотр продукта
@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукт/подробнее'
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': title,
        'object': product,
    }

    return render(request, 'adminapp/product_read.html', context)
