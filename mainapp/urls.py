from django.urls import path

from mainapp.views import products, product

app_name = 'products'

urlpatterns = [
    path('', products, name='products'),
    path('<int:pk>/', products, name='category'),
    path('product/<int:pk>/', product, name='product'),
]
