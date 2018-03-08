# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from datalive_auth.models import UserPermission
from rest_framework.authtoken.models import Token
import json


class UserTests(APITestCase):

    def setUp(self):
        super_user = get_user_model().objects.create_superuser(
            email='developer@thejustbrand.com',
            first_name='Dev',
            last_name='The just brand',
            short_name='xx',
            password='dummy',
            username='developer'
        )
        super_user.permission = UserPermission.objects.create(
            name='Admin Users', is_user=True)
        super_user.save()
        self.token, _ = Token.objects.get_or_create(user=super_user)

    def test_token_auth(self):
        """
        Ensure we can create a get a JWT token using credentials
        """

        # Try to hit the server auth endpoint without token
        url = reverse('server-auth-test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Try again with the token in the header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)