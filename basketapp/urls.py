from django.urls import path

from basketapp import views as basketapp
from basketapp.views import basket

app_name = 'basketapp'

urlpatterns = [
    path('', basket, name='basket'),
    # path('', BasketView.as_view(), name='basket'),
    path('add/<int:pk>/', basketapp.basket_add, name='basket_add'),
    path('remove/<int:pk>/', basketapp.basket_remove, name='basket_remove'),
    path('edit/<int:pk>/<quantity>/', basketapp.basket_edit, name='basket_edit'),

]
