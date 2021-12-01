import json
from datetime import datetime

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from mainapp.models import Product, ProductCategory


def index(request):

    products_list = Product.objects.all()[:4]
    context = {
        'title': 'Магазин',
        'products': products_list,
        'date': datetime.now()
    }
    return render(request, 'mainapp/index.html', context)


with open(f'{settings.BASE_DIR}/mainapp/fixtures/products.json') as file:
    json_product = json.load(file)


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
            'category': category_item
        }

        return render(request, 'mainapp/products_list.html', context)

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
