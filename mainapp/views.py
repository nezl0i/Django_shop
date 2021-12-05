import json
import random
from datetime import datetime

from django.conf import settings
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    product_list = Product.objects.all()
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


with open(f'{settings.BASE_DIR}/mainapp/fixtures/products.json') as file:
    json_product = json.load(file)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    # total_quantity = 0
    # total_sum = 0
    # baskets = Basket.objects.filter(user=request.user)
    # for basket in baskets:
    #     total_sum += basket.sum()
    #     total_quantity += basket.quantity

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
            # 'basket_total': total_quantity,
            # 'basket_price': total_sum

        }

        return render(request, 'mainapp/products_list.html', context)
    hot_product = get_hot_product()
    context = {
        'title': 'Каталог',
        'links_menu': links_menu,
        'products': json_product,
        'hot_product': hot_product,
        'some_products': get_same_products(hot_product),
        'basket': get_basket(request.user)
        # 'basket_total': total_quantity,
        # 'basket_price': total_sum
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    with open(f'{settings.BASE_DIR}/mainapp/fixtures/contacts.json') as f:
        json_contact = json.load(f)
    context = {
        'title': 'Контакты',
        'contacts': json_contact,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context)
