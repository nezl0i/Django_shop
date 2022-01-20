from django.conf import settings
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user} <> Продукт {self.product.name}'

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        items = Basket.objects.filter(user=self.user)
        _total_quantity = sum(list(map(lambda x: x.quantity, items)))
        return _total_quantity

    @property
    def total_cost(self):
        items = Basket.objects.filter(user=self.user).select_related()
        _total_cost = sum(list(map(lambda x: x.product_cost, items)))
        return _total_cost

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)
