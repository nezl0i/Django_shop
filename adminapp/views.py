from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductEditForm
from adminapp.utils import DataMixin
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


# Пользователи CBV
class UsersListView(DataMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'

    def get_context_data(self, **kwargs):
        title = 'Пользователи'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Создание пользователя CBV
class UserCreateView(DataMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_register.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        title = 'Создание пользователя'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Редактирование пользователя CBV
class UserUpdateView(DataMixin,UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminEditForm
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        title = 'Редактирование пользователя'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Удаление пользователя CBV
class UserDeleteView(DataMixin,DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        title = 'Удаление пользователя'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Категории CBV
class CategoriesListView(DataMixin,ListView):
    model = ProductCategory
    template_name = 'adminapp/categories_list.html'

    def get_context_data(self, **kwargs):
        title = 'Категории'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Создание категории CBV
class ProductCategoryCreateView(DataMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, **kwargs):
        title = 'Создание категории'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Редактирование категории CBV
class ProductCategoryUpdateView(DataMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, **kwargs):
        title = 'Редактирование категории'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Удаление категории CBV
class ProductCategoryDeleteView(DataMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, **kwargs):
        title = 'Удаление категории'
        desc = 'категорию'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        context_data['desc'] = desc
        return context_data


# Продукты CBV
class ProductListView(DataMixin, ListView):
    model = Product
    template_name = 'adminapp/products_list.html'

    def get_context_data(self, **kwargs):
        title = 'Товары'
        context_data = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        obj_list = Product.objects.filter(category__pk=category_id)
        context_data['category'] = category_item
        context_data['object_list'] = obj_list
        context_data['title'] = title
        return context_data


# Создание продукта CBV
class ProductCreateView(DataMixin, CreateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('adminapp:categories')

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        title = 'Создание товара'
        context_data = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        context_data['category'] = category_item
        context_data['title'] = title
        return context_data


# Редактирование продукта CBV
class ProductUpdateView(DataMixin, UpdateView):
    model = Product
    template_name = 'adminapp/product_form.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('adminapp:categories')

    def get_success_url(self):
        product_id = self.kwargs.get('pk')
        product_item = get_object_or_404(Product, pk=product_id)
        return reverse('adminapp:products', args=[product_item.category.pk])

    def get_context_data(self, **kwargs):
        title = 'Редактирование товара'
        context_data = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')
        product_item = get_object_or_404(Product, pk=product_id)
        context_data['product'] = product_item
        context_data['title'] = title
        return context_data


# Удаление продукта CBV
class ProductDeleteView(DataMixin, DeleteView):
    model = Product
    template_name = 'adminapp/delete.html'
    success_url = reverse_lazy('adminapp:products')

    def get_success_url(self):
        product_id = self.kwargs.get('pk')
        product_item = get_object_or_404(Product, pk=product_id)
        return reverse('adminapp:products', args=[product_item.category.pk])

    def get_context_data(self, **kwargs):
        title = 'Удаление товара'
        desc = 'товар'
        context_data = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')
        product_item = get_object_or_404(Product, pk=product_id)
        context_data['product'] = product_item
        context_data['title'] = title
        context_data['desc'] = desc
        return context_data


# Просмотр продукта CBV
class ProductDetailView(DataMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        title = 'Товар/подробно'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data
