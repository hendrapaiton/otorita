from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AuthTests(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_and_access_protected_page(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(reverse('protected-page'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_token_cookie = response.client.cookies.get('token')
        self.assertIsNotNone(refresh_token_cookie)

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Selamat datang di Nusantara'})

    def test_refresh_token_from_cookie(self):
        response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        original_access_token = response.data['access']

        self.assertTrue('token' in response.cookies)
        refresh_cookie = response.cookies['token']
        self.assertTrue(refresh_cookie['httponly'])

        response = self.client.post(reverse('token_refresh'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        new_access_token = response.data['access']

        self.assertNotEqual(original_access_token, new_access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + new_access_token)
        response = self.client.get(reverse('protected-page'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials()
        response = self.client.get(reverse('protected-page'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
