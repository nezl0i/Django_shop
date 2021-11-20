from django.shortcuts import render


def index(request):
    context = {
        'title': 'Магазин'
    }
    return render(request, 'mainapp/index.html', context)


def products(request):
    context = {
        'title': 'Каталог'
    }
    return render(request, 'mainapp/products.html', context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context)
