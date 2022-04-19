from django.test import TestCase
from authapp.models import ShopUser
from django.conf import settings


class UserAuthTestCase(TestCase):
    username = 'django'
    password = 'geekbrains'
    email = 'django@gb.local'

    def setUp(self) -> None:
        self.user = ShopUser.objects.create_superuser(
            username=self.username,
            password=self.password,
            email=self.email
        )

    def test_login_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)

    def test_logout_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')

        self.assertFalse(response.context['user'].is_anonymous)
        self.client.get('/auth/logout/')

        self.assertEqual(response.status_code, 200)

        response = self.client.get('/')
        self.assertTrue(response.context['user'].is_anonymous)

    def test_basket_login_redirect(self):
        # без логина должен переадресовать
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)

        # с логином все должно быть хорошо
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')

        self.assertEqual(response.status_code, 200)

    def test_user_register(self):

        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Регистрация')
        self.assertTrue(response.context['user'].is_anonymous)
        new_user_data = {
            'username': 'samuel2',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel2@geekshop.local',
            'age': '21'}
        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

        new_user = ShopUser.objects.get(username=new_user_data['username'])
        activation_url = f"{settings.BASE_URL}/auth/verify/{new_user_data['email']}/{new_user.activation_key}"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)

        self.client.login(username=new_user_data['username'], password=new_user_data['password1'])

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)

        # проверяем главную страницу
        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'], status_code=200)

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'teen',
            'first_name': 'Мэри',
            'last_name': 'Поппинс',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'merypoppins@geekshop.local',
            'age': '17'}

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'age', 'Ваш возраст слишком маленький.')


