from django.core.management import BaseCommand
from django.db.models import Q
from mainapp.models import Product, ProductCategory


class Command(BaseCommand):

    def handle(self, *args, **options):
        home_query = Q(category__name='дом')
        office_query = Q(category__name='офис')

        product_list = Product.objects.filter(home_query | office_query)
        print(product_list)