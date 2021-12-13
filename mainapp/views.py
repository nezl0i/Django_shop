import json
import random
from datetime import datetime

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_json(path: str):
    with open(f'{settings.BASE_DIR}/{path}') as file:
        return json.load(file)


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    product_list = Product.objects.filter(is_active=True)
    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    same_products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_products_list[:3]


def index(request):
    products_list = Product.objects.all()[:4]
    context = {
        'title': 'Магазин',
        'products': products_list,
        'date': datetime.now(),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all()
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk)

        context = {
            'title': 'Каталог',
            'links_menu': links_menu,
            'products': products_list,
            'category': category_item,
            'basket': get_basket(request.user)
        }

        return render(request, 'mainapp/products_list.html', context)
    hot_product = get_hot_product()
    context = {
        'title': 'Каталог',
        'links_menu': links_menu,
        'products': get_json('mainapp/fixtures/products.json'),
        'hot_product': hot_product,
        'some_products': get_same_products(hot_product),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    context = {
        'title': 'Контакты',
        'contacts': get_json('mainapp/fixtures/contacts.json'),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'title': 'Товар',
        'links_menu': links_menu,
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', context)
