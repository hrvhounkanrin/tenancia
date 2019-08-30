# -*- coding: UTF-8 -*-
import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from customuser.models import User
from proprietaire.models import Proprietaire

class ProprietaireAPITestCase(TestCase):

    '''
    Proprietaire API
    '''

    def setUp(self):
        print('Set up test')
        self.client = APIClient()
        #Create and save a user object
        self.user = User.objects.get_or_create(username='ipattey', email='epatey@gmail.com')
      
        
    def test_proprietaire_list(self):
        url = reverse("proprietaire_action")
        #url1 = reverse('proprietaire:proprietaire_action')
        #print('URl 1:{} '.format(url1))
        response = self.client.get(url1)
        response_dict = response.json()
        print(response_dict)
        self.assertIsNotNone(response_dict)
        

    def test_get_proprietaire_returns_correct_fields(self):
        assert False is True

    def test_cannot_create_if_exist(self):
        assert False is True

    def test_societe_users_can_create_proprietaire(self):
        assert False is True

    def test_can_update_prorietaire_data(self):
        assert False is True


class APITest(unittest.TestCase):
    """API Unit Test Class."""

    def setUp(self):
        """Initialize the class with relevant variables."""
        self.client = APIClient()

    def test_api_get(self) -> None:
        """Test Get API."""
        response = self.client.get("/proprietaire_action/create_proprio")
        response_dict = response.json()

        print(response_dict)

        self.assertIsNotNone(response_dict)
