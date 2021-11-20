import json

from django.conf import settings
from django.shortcuts import render


def index(request):
    context = {
        'title': 'Магазин'
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    with open(f'{settings.BASE_DIR}/mainapp/fixtures/products.json') as file:
        json_product = json.load(file)
    context = {
        'title': 'Каталог',
        'products': json_product
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context)
