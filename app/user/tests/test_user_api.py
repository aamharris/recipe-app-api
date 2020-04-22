from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            'email': 'test@test.com',
            'password': 'password',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_already_exists_fails(self):
        payload = {
            'email': 'test@test.com',
            'password': 'password',
            'name': 'Test User'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, 400)

    def test_password_too_short(self):
        payload = {
            'email': 'test@test.com',
            'password': 'pw',
            'name': 'Test User'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, 400)
        user_exists = get_user_model().objects.filter(
                email=payload['email']
            ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        payload = {
            'email': 'test@test.com',
            'password': 'password',
            'name': 'Test User'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, 200)

    def test_invalid_password_no_token(self):
        payload = {
            'email': 'test@test.com',
            'password': 'password',
            'name': 'Test User'
        }
        create_user(**payload)

        invalid_login = {'email': 'test@test.com',
                         'password': 'notright'}

        res = self.client.post(TOKEN_URL, invalid_login)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, 400)
