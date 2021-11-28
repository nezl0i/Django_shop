from django.contrib import admin


from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ShopUser)
