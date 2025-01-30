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
        # Login with username and password
        response = self.client.post(reverse('token_obtain_pair'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']
        
        # Check if the token can be used to access the protected page
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(reverse('protected-page'))  # Changed this line
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if the refresh token cookie is sent
        refresh_token_cookie = response.client.cookies.get('token')
        self.assertIsNotNone(refresh_token_cookie)

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Selamat datang di Nusantara'})
