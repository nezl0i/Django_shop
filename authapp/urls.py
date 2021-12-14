from django.contrib.auth.decorators import login_required
from django.urls import path

from authapp import views as authapp
from authapp.views import UserLoginView, UserRegistrationView, UserProfileView

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('register/', UserRegistrationView.as_view(), name='register'),

]
