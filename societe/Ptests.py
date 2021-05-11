# -*- coding: UTF-8 -*-
"""Mandataire app test case."""
import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from banque.models import Banque
from customuser.models import User
from societe.models import RealEstate


class MandataireAPITestCase(TestCase):
    """Mandatire api test case."""

    def setUp(self):
        """Mandataire api test case setup."""
        self.client = APIClient()
        user_data = {
            "email": "jdegboe@gmail.com",
            "first_name": "Joany",
            "last_name": "DEGBOE",
            "password": "joany",
        }
        self.user = User.objects.get_or_create(user_data)[0]
        banque_data = {"codebanque": "061", "libbanque": "BANK OF ARFICA"}
        self.banque = Banque.objects.get_or_create(banque_data)[0]

    def test_mandataire_can_create(self):
        """Test mandataire can create."""
        self.client.force_authenticate(user=self.user)
        url = "/api/v1/mandataire_action/create_mandataire/"
        mandataire_data = {
            "mandataire": [
                {
                    "raison_social": "GRC IMMOBILIER",
                    "num_telephone": "95415263",
                    "adresse": "Calavi",
                    "logo": "Iconnu",
                    "num_carte_professionnel": "827985656412",
                    "date_delivrance": "2019-01-05",
                }
            ]
        }
        response = self.client.post(url, mandataire_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.status_code == 200, "Expect 201 OK. got: {}".format(
            response.status_code
        )

        assert response.json()["payload"]["societe"][0]
        ["raison_social"] == "GRC IMMOBILIER"

    def test_mandataire_can_update(self):
        """Test mandataire can update."""
        url = "/api/v1/mandataire_action/update_mandataire/"
        mandataire_instance = RealEstate.objects.get_or_create(
            raison_social="GRC IMMOBILIER",
            num_telephone="95415263",
            adresse="Calavi",
            logo="Iconnu",
            num_carte_professionnel="827985656412",
            date_delivrance="2019-01-05",
        )[0]
        mandataire_data = {
            "mandataire": [
                {
                    "id": self.user.id,
                    "raison_social": "MESLEY IMMOBILIER",
                    "num_telephone": "95244000",
                    "adresse": "Calavi",
                    "logo": "Iconnu",
                    "num_carte_professionnel": "827985656412",
                    "date_delivrance": "2019-01-05",
                }
            ]
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            url, json.dumps(mandataire_data), {"id": self.user.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.status_code == 200, "Expect 201 OK. got: {}".format(
            response.status_code
        )
        assert response.json()["payload"]["societe"][0]
        ["raison_social"] == mandataire_instance.raison_social

    def test_mandataire_cannot_create_if_not_login(self):
        """Test not create if not logged in."""
        url = "/api/v1/mandataire_action/create_mandataire"
        mandataire_data = {
            "mandataire": [
                {
                    "raison_social": "GRC IMMOBILIER",
                    "num_telephone": "95415263",
                    "adresse": "Calavi",
                    "logo": "Iconnu",
                    "num_carte_professionnel": "827985656412",
                    "date_delivrance": "2019-01-05",
                }
            ]
        }
        response = self.client.post(url, mandataire_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mandataire_list(self):
        """Get mandataire list."""
        self.client.force_authenticate(user=self.user)
        url = "/api/v1/mandataire_action/get_mandataire"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
