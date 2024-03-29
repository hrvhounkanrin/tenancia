"""Immeuble app test case."""
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from banque.models import Banque
from customuser.models import User
from proprietaire.models import Proprietaire


class ImmeubleAPITestCase(TestCase):
    """Immeuble API Test case."""

    def setUp(self):
        """Immeuble API Setups."""
        self.client = APIClient()
        user_data = {
            "email": "jdegboe@gmail.com",
            "first_name": "Joany",
            "last_name": "DEGBOE",
            "password": "joany",
        }

        self.user = User.objects.get_or_create(user_data)[0]
        banque_data = {
            "codebanque": "061",
            "libbanque": "BANK OF ARFICA",
        }
        self.banque = Banque.objects.get_or_create(banque_data)[0]
        proprietaire_data = {
            "mode_paiement": "VIREMENT BANCAIRE",
            "numcompte": "201515454887",
            "banque_id": self.banque.id,
            "user_id": self.user.id,
        }
        self.proprietaire = Proprietaire.objects.get_or_create(proprietaire_data)[0]

    def test_immeuble_can_create(self):
        """Test immeuble can create."""
        self.client.force_authenticate(user=self.user)
        url = "/api/v1/immeuble_action/create_immeuble"
        immeuble_data = {
            "immeuble": [
                {
                    "intitule": "LEGORF HOME",
                    "description": "Villa",
                    "adresse": "RUE 002 ARCONVILLE",
                    "jour_emission_facture": 5,
                    "jour_valeur_facture": 5,
                    "ville": "CALAVI",
                    "quartier": "CALAVI",
                    "longitude": 0,
                    "latitude": 0,
                    "proprietaire_id": self.proprietaire.id,
                }
            ]
        }
        response = self.client.post(url, immeuble_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert (
            response.status_code == 200
        ), f"Expect 201 OK. got: {response.status_code}"

        assert "LEGORF HOME" == response.json()["payload"]["immeuble"][0]["intitule"]

    def test_immeuble_cannot_create_if_not_login(self):
        """Test immeuble can not create if not logged in."""
        url = "/api/v1/immeuble_action/create_immeuble"
        immeuble_data = {
            "immeuble": [
                {
                    "intitule": "LEGORF HOME",
                    "description": "Villa",
                    "adresse": "RUE 002 ARCONVILLE",
                    "jour_emission_facture": 5,
                    "jour_valeur_facture": 5,
                    "ville": "CALAVI",
                    "quartier": "CALAVI",
                    "longitude": 0,
                    "latitude": 0,
                    "proprietaire_id": self.proprietaire.id,
                }
            ]
        }
        response = self.client.post(url, immeuble_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_immeuble_list(self):
        """Test immeuble get list."""
        self.client.force_authenticate(user=self.user)
        url = "/api/v1/immeuble_action/get_immeuble"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
