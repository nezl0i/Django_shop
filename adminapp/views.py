from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    context = {
        'title': 'Пользователи',
        'object_list': ShopUser.objects.all().order_by('-is_active'),
    }
    return render(request, 'adminapp/users_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': 'Создание пользователя',
        'form': user_form
    }
    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    # ShopUserAdminEditForm
    pass


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'title': 'Категории товаров',
        'object_list': ProductCategory.objects.all()
    }

    return render(request, 'adminapp/categories_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    pass


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    context = {
        'title': 'Товары',
        'object_list': Product.objects.filter(category__pk=pk)
    }

    return render(request, 'adminapp/products_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request):
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    pass
