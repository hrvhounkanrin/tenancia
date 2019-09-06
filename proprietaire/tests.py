# -*- coding: UTF-8 -*-
"""Proprietaire API test case."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from banque.models import Banque
from customuser.models import User
from proprietaire.models import Proprietaire


class ProprietaireAPITestCase(TestCase):
    """Proprietaire API TestCase."""

    def setUp(self):
        """Proprietaire api testcase setup."""
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

    def test_proprietaire_can_create(self):
        """Test proprietaire can create."""
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/proprietaire_action/create_proprio'
        proprietaire_data = {
            'proprietaire': [
                {
                    'mode_paiement': 'VIREMENT BANCAIRE',
                    'numcompte': '201515454887',
                    'banque_id': self.banque.id,
                    'user_id': self.user.id
                }
            ]
        }
        response = self.client.post(url, proprietaire_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.status_code == 200, \
            'Expect 201 OK. got: {}' . format(response.status_code)
        assert response.json()['payload']['proprietaire'][0]
        ['numcompte'] == '201515454887'

    def test_proprietaire_cannot_create_if_not_login(self):
        """Test proprietaire can not create if not logged in."""
        url = '/api/v1/proprietaire_action/create_proprio'
        proprietaire_data = {
            'proprietaire': [
                {
                    'mode_paiement': 'VIREMENT BANCAIRE',
                    'numcompte': '201515454887',
                    'banque_id': self.banque.id,
                    'user_id': self.user.id
                }
            ]
        }
        response = self.client.post(url, proprietaire_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_proprietaire_cannot_duplicated(self):
        """Test proprietaire can not create if not logged in."""
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/proprietaire_action/create_proprio'
        proprietaire_data = {
            'proprietaire': [
                {
                    'mode_paiement': 'VIREMENT BANCAIRE',
                    'numcompte': '201515454887',
                    'banque_id': self.banque.id,
                    'user_id': self.user.id
                }
            ]
        }
        Proprietaire.objects.get_or_create(
            proprietaire_data['proprietaire'][0])[0]
        response = self.client.post(url, proprietaire_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_proprietaire_list(self):
        """Test proprietaire list."""
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/proprietaire_action/get_proprio'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
