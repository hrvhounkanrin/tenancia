"""Immeuble app test case."""
import logging
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from banque.models import Banque
from customuser.models import User
from proprietaire.models import Proprietaire

logger = logging.getLogger(__name__)

class ImmeubleAPITestCase(TestCase):
    """Immeuble API Test case."""
    fixtures = ["country.json"]

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

        self.immeuble_data = {
            "intitule": "LES HIBISCUS",
            "description": "RAS",
            "adresse": "Agla, agongbomey",
            "jour_emission_facture": 5,
            "jour_valeur_facture": 5,
            "ville": "COTONOU",
            "quartier": "Agla",
            "pays": "BJ",
            "longitude": 0,
            "latitude": 0,
            "proprietaire_id": self.proprietaire.id
        }

    def test_immeuble_can_create(self):
        """Test immeuble can create."""
        self.client.force_authenticate(user=self.user)
        url = "/api/v1/immeuble_action/create_immeuble"

        response = self.client.post(url, self.immeuble_data, format="json")
        logger.debug(response.json()["payload"])
        assert (
            response.status_code == 200
        ), f"Expect 200 OK. got: {response.status_code}"

        # assert "LES HIBISCUS" == response.json()["payload"]["intitule"]

    def test_immeuble_cannot_create_if_not_login(self):
        """Test immeuble can not create if not logged in."""
        url = "/api/v1/immeuble_action/create_immeuble"

        response = self.client.post(url, self.immeuble_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
