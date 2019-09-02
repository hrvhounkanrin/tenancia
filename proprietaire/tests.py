# -*- coding: UTF-8 -*-
import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from customuser.models import User
from proprietaire.models import Proprietaire
from banque.models import Banque
from rest_framework.test import force_authenticate
from rest_framework import status
from pprint import pprint
from rest_framework.authtoken.models import Token
from countries_plus.models import Country

class ProprietaireAPITestCase(TestCase):

    '''
    Proprietaire API
    '''

    def setUp(self):
        self.client = APIClient()
        user_data={
            'email':'jdegboe@gmail.com',
            'first_name': 'Joany',
            'last_name': 'DEGBOE',
            'password':'joany'
        }
        
        self.user=User.objects.get_or_create(user_data)[0]
        
        banque_data={
            'codebanque':'061',
            'libbanque': 'BANK OF ARFICA',
        }
        self.banque=Banque.objects.get_or_create(banque_data)[0]

    def test_proprietaire_can_create(self):
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/proprietaire_action/create_proprio'
        proprietaire_data={
            'proprietaire':[
                {
                    'mode_paiement': 'VIREMENT BANCAIRE',
                    'numcompte': '201515454887',
                    'banque_id':self.banque.id,
                    'user_id':self.user.id
                }
            ]
        }
        response = self.client.post(url, proprietaire_data,format='json')
        response_dict = response.json()
        #print(response_dict['payload']['proprietaire'][0]['numcompte'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.status_code == 200, \
            "Expect 201 OK. got: {}" . format(response.status_code)
            
        assert response.json()["payload"]['proprietaire'][0]['numcompte'] == "201515454887"

    def test_proprietaire_cannot_create_if_not_login(self):
        url = '/api/v1/proprietaire_action/create_proprio'
        proprietaire_data={
            'proprietaire':[
                {
                    'mode_paiement': 'VIREMENT BANCAIRE',
                    'numcompte': '201515454887',
                    'banque_id':self.banque.id,
                    'user_id':self.user.id
                }
            ]
        }
        response = self.client.post(url, proprietaire_data,format='json')
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_proprietaire_cannot_duplicated(self):
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/proprietaire_action/create_proprio'
        proprietaire_data={
            'proprietaire':[
                {
                    'mode_paiement': 'VIREMENT BANCAIRE',
                    'numcompte': '201515454887',
                    'banque_id':self.banque.id,
                    'user_id':self.user.id
                }
            ]
        }
        Proprietaire.objects.get_or_create(proprietaire_data['proprietaire'][0])[0]
        response = self.client.post(url, proprietaire_data,format='json')
        response_dict = response.json()
        print(response_dict)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
       

    def test_proprietaire_list(self):
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/proprietaire_action/get_proprio'
        response = self.client.get(url)
        #response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)