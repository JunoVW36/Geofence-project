# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from datalive_auth.models import UserPermission, ModulePermission
from google.appengine.ext import testbed
import json


class UserTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.testbed = testbed.Testbed()
        cls.testbed.activate()
        cls.testbed.init_urlfetch_stub()
        cls.testbed.init_mail_stub()

    @classmethod
    def tearDownClass(cls):
        cls.testbed.deactivate()

    def setUp(self):
        self.super_user = get_user_model().objects.create_superuser(
            email='developer@thejustbrand.com',
            first_name='Dev',
            last_name='The just brand',
            short_name='xx',
            password='dummy',
            username='developer'
        )

        self.u_perm1 = UserPermission.objects.create(
            name='Admin Users', is_global_admin=True, is_limited_user=False)
        self.super_user.permission = self.u_perm1
        self.super_user.save()

        self.m_perm1 = ModulePermission.objects.create(
            name='Track Module', description='Track Module')
        self.m_perm2 = ModulePermission.objects.create(
            name='Defect Module', description='Defect Module')

    def get_jwt_token(self):
        # First try logging in through email
        login_data = {
            'email': 'developer@thejustbrand.com',
            'password': 'dummy'
        }
        response = self.client.post(
            '/api/authenticate', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return json.loads(response.content)['token']

    def test_generate_jwt(self):
        """
        Ensure we can create a get a JWT token using credentials
        """
        url = '/api/authenticate'

        # First try logging in through email
        login_data = {
            'email': 'developer@thejustbrand.com',
            'password': 'dummy'
        }
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now try logging in using the username
        login_data = {
            'username': 'developer',
            'password': 'dummy'
        }
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if we can access a protected view using the token
        token = json.loads(response.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_create_user(self):
        """
            Ensure that we are able to get a list of modules
        """
        self.client.force_authenticate(user=self.super_user)

        url = reverse('user-list')
        post_data = {
            'email': 'developer2@thejustbrand.com',
            'first_name': 'Dev2',
            'last_name': 'the just brand',
            'modules': [{
                'id': self.m_perm1.id,
                'name': self.m_perm1.name
            }],
            'customers': [],
            'groups': [],
            'permission': self.u_perm1.name,
        }
        response = self.client.post(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['modules'][0]['id'], self.m_perm1.id)

    def test_update_user(self):
        """
            Ensure that we are able to get a list of modules
        """
        self.client.force_authenticate(user=self.super_user)

        url = '/api/user/{}/'.format(self.super_user.id)
        post_data = {
            'email': 'developer2@thejustbrand.com',
            'first_name': 'Dev2',
            'last_name': 'the just brand',
            'modules': [
                {
                    'id': self.m_perm2.id,
                    'name': self.m_perm2.name
                }
            ],
        }

        response = self.client.put(url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['modules'][0]['id'], self.m_perm2.id)

    def test_module_list(self):
        """
        Ensure that we are able to get a list of modules
        """
        self.client.force_login(user=self.super_user)

        url = reverse('module-permissions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_response = [
            {
                'id': self.m_perm1.id,
                'name': self.m_perm1.name
            },
            {
                'id': self.m_perm2.id,
                'name': self.m_perm2.name
            }
        ]

        self.assertListEqual(expected_response, response.json())

