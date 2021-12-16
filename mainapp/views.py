import json
import random
from datetime import datetime

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

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


class IndexView(ListView):
    model = Product
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        products_list = Product.objects.all()[:4]

        context_data['title'] = 'Магазин'
        context_data['date'] = datetime.now()
        context_data['products'] = products_list
        context_data['basket'] = get_basket(self.request.user)
        return context_data


def products(request, pk=None, page=1):
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.filter(is_active=True, category__is_active=True)
            category_item = {'name': 'Все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk, is_active=True)

        # page = request.GET.get('page', 1)
        paginator = Paginator(products_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)  # Or return 404

        context = {
            'title': 'Каталог',
            'links_menu': links_menu,
            'products': products_paginator,
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


class ContactViews(ListView):
    template_name = 'mainapp/contact.html'
    title = 'Контакты'

    def get_queryset(self):
        contacts = get_json('mainapp/fixtures/contacts.json')
        return contacts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['contacts'] = self.get_queryset()
        context['basket'] = get_basket(self.request.user)
        return context


class ProductView(ListView):
    model = Product
    template_name = 'mainapp/product.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        links_menu = ProductCategory.objects.all()
        product_id = self.kwargs.get('pk')
        product = get_object_or_404(Product, pk=product_id)
        context_data['title'] = 'Товар'
        context_data['links_menu'] = links_menu
        context_data['product'] = product
        context_data['basket'] = get_basket(self.request.user)
        return context_data

# def index(request):
#     products_list = Product.objects.all()[:4]
#     context = {
#         'title': 'Магазин',
#         'products': products_list,
#         'date': datetime.now(),
#         'basket': get_basket(request.user)
#     }
#     return render(request, 'mainapp/index.html', context)

# def product(request, pk):
#     links_menu = ProductCategory.objects.all()
#     context = {
#         'title': 'Товар',
#         'links_menu': links_menu,
#         'product': get_object_or_404(Product, pk=pk),
#         'basket': get_basket(request.user)
#     }
#     return render(request, 'mainapp/product.html', context)

# def contact(request):
#     context = {
#         'title': 'Контакты',
#         'contacts': get_json('mainapp/fixtures/contacts.json'),
#         'basket': get_basket(request.user)
#     }
#     return render(request, 'mainapp/contact.html', context)
