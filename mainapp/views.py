import json
import random
from datetime import datetime

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True,category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_json(path: str):
    with open(f'{settings.BASE_DIR}/{path}') as file:
        return json.load(file)


def get_hot_product():
    product_list = get_products()
    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    same_products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_products_list[:3]


class IndexView(ListView):
    model = Product
    template_name = 'mainapp/index.html'
    title = 'GeekShop'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.title
        context_data['date'] = datetime.now()
        context_data['products'] = get_products()[:4]
        return context_data


@cache_page(3600)
def products(request, pk=None, page=1):
    links_menu = get_links_menu()

    if pk is not None:
        if pk == 0:
            # products_list = Product.objects.filter(is_active=True, category__is_active=True)
            products_list = get_products_ordered_by_price()
            category_item = {'name': 'Все', 'pk': 0}
        else:
            # category_item = get_object_or_404(ProductCategory, pk=pk)
            category_item = get_category(pk)
            products_list = get_products_in_category_ordered_by_price(pk)

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
        }

        return render(request, 'mainapp/products_list.html', context)
    hot_product = get_hot_product()
    context = {
        'title': 'Каталог',
        'links_menu': links_menu,
        'products': get_json('mainapp/fixtures/products.json'),
        'hot_product': hot_product,
        'some_products': get_same_products(hot_product),
    }
    return render(request, 'mainapp/products.html', context)


class ContactViews(ListView):
    template_name = 'mainapp/contact.html'
    title = 'Контакты'

    def get_queryset(self):
        if settings.LOW_CACHE:
            key = f'contacts'
            contacts = cache.get(key)
            if contacts is None:
                contacts = get_json('mainapp/fixtures/contacts.json')
                cache.set(key, contacts)
            return contacts
        else:
            return get_json('mainapp/fixtures/contacts.json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['contacts'] = self.get_queryset()
        return context


class ProductView(ListView):
    model = Product
    template_name = 'mainapp/product.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        links_menu = get_links_menu()
        product_id = self.kwargs.get('pk')
        # product = get_object_or_404(Product, pk=product_id)
        product = get_product(product_id)
        context_data['title'] = 'Товар'
        context_data['links_menu'] = links_menu
        context_data['product'] = product
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
