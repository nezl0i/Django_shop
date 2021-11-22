import json
from datetime import datetime

from django.conf import settings
from django.shortcuts import render


def index(request):
    context = {
        'title': 'Магазин',
        'date': datetime.now()
    }
    return render(request, 'mainapp/index.html', context)


links_menu = [
    {'href': 'products', 'name': 'Все'},
    {'href': 'products_home', 'name': 'Дом'},
    {'href': 'products_modern', 'name': 'Модерн'},
    {'href': 'products_office', 'name': 'Офис'},
    {'href': 'products_classic', 'name': 'Классика'},
]

with open(f'{settings.BASE_DIR}/mainapp/fixtures/products.json') as file:
    json_product = json.load(file)


def products(request):
    context = {
        'title': 'Каталог',
        'links_menu': links_menu,
        'products': json_product
    }
    return render(request, 'mainapp/products.html', context)


def products_home(request):
    context = {
        'title': 'Каталог',
        'links_menu': links_menu,
        'products': json_product
    }
    return render(request, 'mainapp/products.html', context)


def products_modern(request):
    context = {
        'title': 'Каталог',
        'links_menu': links_menu,
        'products': json_product
    }
    return render(request, 'mainapp/products.html', context)


def products_office(request):
    context = {
        'title': 'Каталог',
        'links_menu': links_menu,
        'products': json_product
    }
    return render(request, 'mainapp/products.html', context)


def products_classic(request):
    context = {
        'title': 'Каталог',
        'links_menu': links_menu,
        'products': json_product
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/mainapp/fixtures/contacts.json') as f:
        json_contact = json.load(f)
    context = {
        'title': 'Контакты',
        'contacts': json_contact
    }
    return render(request, 'mainapp/contact.html', context)
