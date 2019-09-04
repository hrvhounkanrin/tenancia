# -*- coding: UTF-8 -*-
import unittest
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from customuser.models import User
from societe.models import Societe
from banque.models import Banque
from rest_framework.test import force_authenticate
from rest_framework import status
from pprint import pprint
from rest_framework.authtoken.models import Token
from countries_plus.models import Country

class MandataireAPITestCase(TestCase):

    '''
    mandataire API
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
    
    def test_mandataire_can_create(self):
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/mandataire_action/create_mandataire/'
        mandataire_data = {
            'mandataire':[
                {
                    'raison_social': 'GRC IMMOBILIER',
                    'num_telephone': '95415263',
                    'adresse': 'Calavi',
                    'logo': 'Iconnu',
                    'num_carte_professionnel': '827985656412',
                    'date_delivrance': '2019-01-05'
                }
            ]
        }
        response = self.client.post(url, mandataire_data,format='json')
        #print(response.data)
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.status_code == 200, \
            'Expect 201 OK. got: {}' . format(response.status_code)
            
        assert response.json()['payload']['societe'][0]['raison_social'] == 'GRC IMMOBILIER'

    def test_mandataire_can_update(self):
        
        url = '/api/v1/mandataire_action/update_mandataire/'
        mandataire_instance = Societe.objects.get_or_create(
            raison_social='GRC IMMOBILIER',
            num_telephone= '95415263',
            adresse= 'Calavi',
            logo= 'Iconnu',
            num_carte_professionnel='827985656412',
            date_delivrance= '2019-01-05')[0]
        
        mandataire_data = {
            'mandataire':[
                {
                    'id':self.user.id,
                    'raison_social': 'MESLEY IMMOBILIER',
                    'num_telephone': '95244000',
                    'adresse': 'Calavi',
                    'logo': 'Iconnu',
                    'num_carte_professionnel': '827985656412',
                    'date_delivrance': '2019-01-05'
                }
            ]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, json.dumps(mandataire_data), {'id': self.user.id})
        response_dict = response.json()
        #print(response_dict['payload']['mandataire'][0]['numcompte'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.status_code == 200, \
            'Expect 201 OK. got: {}' . format(response.status_code)
            
        assert response.json()['payload']['societe'][0]['raison_social'] == 'MESLEY IMMOBILIER'

    def test_mandataire_cannot_create_if_not_login(self):
        url = '/api/v1/mandataire_action/create_mandataire'
        mandataire_data={
            'mandataire':[
                {
                    'raison_social': 'GRC IMMOBILIER',
                    'num_telephone': '95415263',
                    'adresse': 'Calavi',
                    'logo': 'Iconnu',
                    'num_carte_professionnel': '827985656412',
                    'date_delivrance': '2019-01-05'
                }
            ]
        }
        #print(mandataire_data)
        response = self.client.post(url, mandataire_data,format='json')
        #print(response.data)
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_mandataire_list(self):
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/mandataire_action/get_mandataire'
        response = self.client.get(url)
        #response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)