# -*- coding: UTF-8 -*-
from django.test import TestCase, Client
from customuser.models import User
from proprietaire.models import Proprietaire

class ProprietaireAPITestCase(TestCase):

    '''
    Proprietaire API
    '''

    def setUp(self):
        self.c = Client()
        #Create and save a user object
        self.user = User(username='ipattey', email='epatey@gmail.com').save()
        self.user, created = Person.objects.get_or_create(
            {
                email:'ipattey@gmail.com', first_name: 'Pattey', last_name: 'ISMAEL',
                password:'ipattey',  profile:{
                    title: 'IT', dob: '1986-05-09', address: 'UNKOWN', country: 'BJ',
                    zip: '093', city: 'COTONOU'
                }
            t
        t

   tdeet_proprietaire_lise(self):
        assert False is True

    def test_get_proprietaire_returns_correct_fields(self):
        assert False is True

    def test_cannot_create_if_exist(self):
        assert False is True

    def test_societe_users_can_create_proprietaire(self):
        assert False is True

    def test_can_update_prorietaire_data(self):
        assert False is True