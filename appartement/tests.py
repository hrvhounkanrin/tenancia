# -*- coding: UTF-8 -*-
import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from customuser.models import User
from proprietaire.models import Proprietaire
from immeuble.models import Immeuble
from appartement.models import Appartement
from banque.models import Banque
from appartement.models import ComposantAppartement
from rest_framework.test import force_authenticate
from rest_framework import status
from pprint import pprint
from rest_framework.authtoken.models import Token
from countries_plus.models import Country

class AppartementAPITestCase(TestCase):

    '''
    Appartement API
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
        proprietaire_data={
            'mode_paiement': 'VIREMENT BANCAIRE',
            'numcompte': '201515454887',
            'banque_id':self.banque.id,
            'user_id':self.user.id
        }
        self.proprietaire = Proprietaire.objects.get_or_create(proprietaire_data)[0]
        immeuble_data={
                        "intitule": "LEGORF HOME",
                        "description": "Villa",
                        "adresse": "RUE 002 ARCONVILLE",
                        "jour_emission_facture": 5,
                        "jour_valeur_facture": 5,
                        "ville": "CALAVI",
                        "quartier": "CALAVI",
                        "longitude": 0,
                        "latitude": 0,
                        "proprietaire_id":self.proprietaire.id
        }
        self.immeuble=Immeuble.objects.get_or_create(immeuble_data)[0]
        """Composant appartement"""
        self.composant1=ComposantAppartement.objects.get_or_create(libelle='LIVING ROOM', utilite='salon')[0]
        self.composant2=ComposantAppartement.objects.get_or_create(libelle='BED ROOMS', utilite='Chambre à coucher')[0]
        self.composant3=ComposantAppartement.objects.get_or_create(libelle='KITCHEN', utilite='Cuisine')[0]

    def test_logement_can_create(self):
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/logement_action/create_logement'
        housing_data = {
            "intitule": "ST XX",
            "level": 1,
            "autre_description": "Chaque chambre avec sa douche avec une douche visiteur en plus",
            "statut": "LIBRE",
            "immeuble_id": 1,
            "structures": [
            {
                    "composantAppartement": self.composant1.id,
                    "nbre":1,
                    "description": "Le salon de l'appartement"
                },
                {
                    "composantAppartement": self.composant2.id,
                    "nbre":3,
                    "description": "Les trois chambres de l'appartement"
                },
                {
                    "composantAppartement": self.composant3.id,
                    "nbre":1,
                    "description": "La seule cuisie de l'appartement"
                }
            ]
        
        }
        response = self.client.post(url, housing_data,format='json')
        #print(response.data)
        response_dict = response.json()
        #print(response_dict['payload']['proprietaire'][0]['numcompte'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.status_code == 200, \
            "Expect 201 OK. got: {}" . format(response.status_code)
            
        assert response.json()["payload"]['appartement']['intitule'] == "ST XX"

    def test_logement_cannot_create_if_not_login(self):
        url = '/api/v1/logement_action/create_appartment'
        housing_data = {
            "intitule": "ST XX",
            "level": 1,
            "autre_description": "Chaque chambre avec sa douche avec une douche visiteur en plus",
            "statut": "LIBRE",
            "immeuble_id": 1,
            "structures": [
            {
                    "composantAppartement": self.composant1.id,
                    "nbre":1,
                    "description": "Le salon de l'appartement"
                },
                {
                    "composantAppartement": self.composant2.id,
                    "nbre":3,
                    "description": "Les trois chambres de l'appartement"
                },
                {
                    "composantAppartement": self.composant3.id,
                    "nbre":1,
                    "description": "La seule cuisie de l'appartement"
                }
            ]
        
        }
        response = self.client.post(url, housing_data,format='json')
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
   
       

    def test_logement_list(self):
        self.client.force_authenticate(user=self.user)
        url = '/api/v1/logement_action/get_logement'
        response = self.client.get(url)
        #response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)