from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView

from basketapp.models import Basket
from mainapp.models import Product


# @login_required
# def basket(request):
#     context = {
#         'title': 'Корзина',
#         'basket_list': Basket.objects.filter(user=request.user)
#
#     }
#     return render(request, 'basketapp/basket.html', context)

class BasketView(ListView):
    model = Basket
    template_name = 'basketapp/basket.html'
    success_url = reverse_lazy('basketapp:basket')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Корзина'
        context_data['basket_list'] = Basket.objects.filter(user=self.request.user).select_related()
        return context_data


@login_required
def basket_add(request, pk):  # pk - Product.pk
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product_item = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(user=request.user, product=product_item).first()
    if not basket_item:
        basket_item = Basket(
            user=request.user,
            product=product_item
        )

    basket_item.quantity += 1
    basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):  # pk - Basket.pk
    basket_item = get_object_or_404(Basket, pk=pk)
    basket_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# class BasketRemoveView(DeleteView):
#     model = Basket
#     template_name = 'basketapp/basket.html'
#     success_url = reverse_lazy('basket:remove')
#
#     def get_success_url(self):
#         product_id = self.kwargs.get('pk')
#         product_item = get_object_or_404(Basket, pk=product_id)
#         product_item.delete()
#         return reverse('basket:remove', args=[product_item.pk])


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket_item = Basket.objects.get(pk=pk)

        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
        else:
            basket_item.delete()

        basket_list = Basket.objects.filter(user=request.user)
        result = render_to_string('basketapp/user_profile_basket.html', {'basket_list': basket_list})
        return JsonResponse({'result': result})
