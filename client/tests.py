# -*- coding: UTF-8 -*-
"""Client app tests."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from banque.models import Banque
from client.models import Client
from customuser.models import User


class ClientAPITestCase(TestCase):
    """Cient API tests."""

    def setUp(self):
        """Initilizing client api test case."""
        self.client = APIClient()
        user_data = {
            'email': 'jdegboe@gmail.com',
            'first_name': 'Joany',
            'last_name': 'DEGBOE',
            'password': 'joany'
        }
        self.user = User.objects.get_or_create(user_data)[0]
        banque_data = {
            'codebanque': '061',
            'libbanque': 'BANK OF ARFICA',
        }
        self.banque = Banque.objects.get_or_create(banque_data)[0]

    def test_client_can_create(self):
        """Test client can create api."""
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/client_action/create_client'
        client_data = {
            "phone_number": "9834434",
            "profession": "Financiere",
            "ice_contact": "BOCOVO Ghislaine",
            "ice_number": "97819436",
            "ice_relation": "GRANDE SOEUR"
        }
        response = self.client.post(url, client_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.status_code == 200, \
            'Expect 200 OK. got: {}' . format(response.status_code)
        assert '97819436' == \
               response.json()['payload']['ice_number']

    def test_client_cannot_create_if_not_login(self):
        """Client client can not test if not log in."""
        url = '/api/v1/client_action/create_client'
        client_data = {
            "phone_number": "9834434",
            "profession": "Financiere",
            "ice_contact": "BOCOVO Ghislaine",
            "ice_number": "97819436",
            "ice_relation": "GRANDE SOEUR"
        }
        response = self.client.post(url, client_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_cannot_duplicated(self):
        """Test client can not be duplicated."""
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/client_action/create_client'
        client_data = {
            "phone_number": "9834434",
            "profession": "Financiere",
            "ice_contact": "BOCOVO Ghislaine",
            "ice_number": "97819436",
            "ice_relation": "GRANDE SOEUR"
        }

        response_1 = self.client.post(url, client_data, format='json')
        assert response_1.status_code == 200, \
            'Expect 200 OK. got: {}'.format(response_1.status_code)
        response_2 = self.client.post(url, client_data, format='json')
        assert response_2.status_code == 400, \
            'Expect 400 OK. got: {}'.format(response_2.status_code)

    def test_client_list(self):
        """Test client api list."""
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/client_action/get_client'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
