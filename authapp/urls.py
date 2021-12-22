from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from authapp import views as authapp
from authapp.views import UserLoginView, UserProfileView, UserLogoutView, verify, UserRegistrationView

app_name = 'authapp'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    # path('register/', register, name='register'),
    path('verify/<email>/<activation_key>', verify, name='verify'),

]
