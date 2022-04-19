from django.db.models import F
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductEditForm
from adminapp.utils import DataMixin
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


# Пользователи CBV
from ordersapp.models import Order


class UsersListView(DataMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Пользователи'
        return context_data


# Заказы CBV
class OrderListView(ListView):
    model = Order
    template_name = 'adminapp/order_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Заказы'
        return context_data


# Создание пользователя CBV
class UserCreateView(DataMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_register.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание пользователя'
        return context_data


# Редактирование пользователя CBV
class UserUpdateView(DataMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminEditForm
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование пользователя'
        return context_data


# Удаление пользователя CBV
class UserDeleteView(DataMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление пользователя'
        return context_data


# Категории CBV
class CategoriesListView(DataMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Категории'
        return context_data


# Создание категории CBV
class ProductCategoryCreateView(DataMixin, CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание категории'
        return context_data


# Редактирование категории CBV
class ProductCategoryUpdateView(DataMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Редактирование категории'
        return context_data

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price'))

        return super().form_valid(form)


# Удаление категории CBV
class ProductCategoryDeleteView(DataMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Удаление категории'
        context_data['desc'] = 'категорию'
        return context_data


# Продукты CBV
class ProductListView(DataMixin, ListView):
    model = Product
    template_name = 'adminapp/products_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        obj_list = Product.objects.filter(category__pk=category_id)
        context_data['category'] = category_item
        context_data['object_list'] = obj_list
        context_data['title'] = 'Товары'
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
        context_data = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category_item = get_object_or_404(ProductCategory, pk=category_id)
        context_data['category'] = category_item
        context_data['title'] = 'Создание товара'
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
        context_data = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')
        product_item = get_object_or_404(Product, pk=product_id)
        context_data['product'] = product_item
        context_data['title'] = 'Редактирование товара'
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
        context_data = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('pk')
        product_item = get_object_or_404(Product, pk=product_id)
        context_data['product'] = product_item
        context_data['title'] = 'Удаление товара'
        context_data['desc'] = 'товар'
        return context_data


# Просмотр продукта CBV
class ProductDetailView(DataMixin, DeleteView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Товар/подробно'
        return context_data
