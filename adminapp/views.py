from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


# Пользователи CBV
class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users_list.html'

    def get_context_data(self, **kwargs):
        title = 'Пользователи'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)


# Создание пользователя CBV
class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_register.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('adminapp:users')

    def get_context_data(self, **kwargs):
        title = 'Создание пользователя'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)


# Редактирование пользователя CBV
class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_form.html'
    form_class = ShopUserAdminEditForm
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)

    def get_context_data(self, **kwargs):
        title = 'Редактирование пользователя'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Удаление пользователя CBV
class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('adminapp:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)

    def get_context_data(self, **kwargs):
        title = 'Удаление пользователя'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Категории CBV
class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories_list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)

    def get_context_data(self, **kwargs):
        title = 'Категории'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Создание категории CBV
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)

    def get_context_data(self, **kwargs):
        title = 'Создание категории'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Редактирование категории CBV
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_form.html'
    form_class = ProductCategoryForm
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)

    def get_context_data(self, **kwargs):
        title = 'Редактирование категории'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


# Удаление категории CBV
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/delete.html'
    success_url = reverse_lazy('adminapp:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)

    def get_context_data(self, **kwargs):
        title = 'Удаление категории'
        desc = 'категорию'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        context_data['desc'] = desc
        return context_data


# Продукты CBV
class ProductListView(ListView):
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

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)


# Создание продукта CBV
class ProductCreateView(CreateView):
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

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)


# Редактирование продукта CBV
class ProductUpdateView(UpdateView):
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

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)


# Удаление продукта CBV
class ProductDeleteView(DeleteView):
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

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)


# Просмотр продукта CBV
class ProductDetailView(DeleteView):
    model = Product
    template_name = 'adminapp/product_read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args)

    def get_context_data(self, **kwargs):
        title = 'Товар/подробно'
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = title
        return context_data


#  ==========================     ======================================
# Пользователи
# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     context = {
#         'title': 'Пользователи',
#         'object_list': ShopUser.objects.all().order_by('-is_active'),
#     }
#     return render(request, 'adminapp/users_list.html', context)

# Создание пользователя
# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     if request.method == 'POST':
#         form = ShopUserRegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:users'))
#     else:
#         form = ShopUserRegisterForm()
#
#     context = {
#         'title': 'Создание пользователя',
#         'form': form,
#
#     }
#     return render(request, 'adminapp/user_register.html', context)

# Удаление пользователя
# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     current_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         current_user.is_active = False
#         current_user.save()
#         return HttpResponseRedirect(reverse('adminapp:users'))
#     context = {
#         'title': 'Удаление пользователя',
#         'object': current_user
#     }
#     return render(request, 'adminapp/user_delete.html', context)

# Редактирование пользователя
# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     selected_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         form = ShopUserAdminEditForm(request.POST, instance=selected_user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:users'))
#     else:
#         form = ShopUserAdminEditForm(instance=selected_user)
#     context = {
#         'title': 'Редактирование пользователя',
#         'form': form,
#         'user': selected_user,
#     }
#     return render(request, 'adminapp/user_form.html', context)
# Категории
# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     context = {
#         'title': 'Категории товаров',
#         'object_list': ProductCategory.objects.all()
#     }
#
#     return render(request, 'adminapp/categories_list.html', context)

# Создание категории
# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         form = ProductCategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         form = ProductCategoryForm()
#
#     context = {
#         'title': 'Создание категории',
#         'form': form,
#     }
#     return render(request, 'adminapp/category_create.html', context)

# Редактирование категории
# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         form = ProductCategoryForm(request.POST, instance=category_item)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:categories'))
#     else:
#         form = ProductCategoryForm(instance=category_item)
#
#     context = {
#         'title': 'Изменение категории',
#         'form': form,
#         'item': category_item,
#     }
#     return render(request, 'adminapp/category_form.html', context)

# Удаление категории
# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         category_item.is_active = False
#         category_item.save()
#         return HttpResponseRedirect(reverse('adminapp:categories'))
#     context = {
#         'title': 'Удаление категории',
#         'desc': 'категорию',
#         'object': category_item
#     }
#     return render(request, 'adminapp/delete.html', context)

# Продукты
# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     context = {
#         'title': 'Товары',
#         'object_list': Product.objects.filter(category__pk=pk),
#         'category': category_item
#     }
#
#     return render(request, 'adminapp/products_list.html', context)

# Создание продукта
# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         form = ProductEditForm(request.POST, request.FILES)
#         if form.is_valid():
#             product_item = form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category.pk]))
#     else:
#         form = ProductEditForm()
#
#     context = {
#         'title': 'Создание товара',
#         'form': form,
#         'category': category_item
#     }
#     return render(request, 'adminapp/product_form.html', context)

# Редактирование продукта
# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         form = ProductEditForm(request.POST, request.FILES, instance=product_item)
#         if form.is_valid():
#             product_item = form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category.pk]))
#     else:
#         form = ProductEditForm(instance=product_item)
#
#     context = {
#         'title': 'Редактирование товара',
#         'form': form,
#         'product': product_item
#     }
#     return render(request, 'adminapp/product_form.html', context)

# Удаление продукта
# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         product_item.is_active = False
#         product_item.save()
#         return HttpResponseRedirect(reverse('adminapp:products', args=[product_item.category.pk]))
#     context = {
#         'title': 'Удаление товара',
#         'desc': 'товар',
#         'object': product_item
#     }
#     return render(request, 'adminapp/delete.html', context)

# Просмотр продукта
# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'Продукт/подробно'
#     product = get_object_or_404(Product, pk=pk)
#     context = {
#         'title': title,
#         'object': product,
#     }
#
#     return render(request, 'adminapp/product_read.html', context)
