from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_for_users')
def media_for_users(avatar):
    if not avatar:
        avatar = 'users/default_avatar.jpg'

    return f'{settings.MEDIA_URL}{avatar}'


def media_for_products(image):
    if not image:
        image = 'products_img/product-21.jpg'

    return f'{settings.MEDIA_URL}{image}'


register.filter('media_for_products', media_for_products)

