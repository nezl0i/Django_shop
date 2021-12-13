from django.urls import path

from mainapp.views import products, product

app_name = 'products'

urlpatterns = [
    path('', products, name='products'),
    path('<int:pk>/', products, name='category'),
    path('<int:pk>/<int:page>/', products, name='products_paginate'),
    path('product/<int:pk>/', product, name='product'),

]
