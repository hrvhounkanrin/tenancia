"""Proprietaire API test case."""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from banque.models import Banque
from customuser.models import User
from proprietaire.models import Proprietaire


class ProprietaireAPITestCase(TestCase):
    """Proprietaire API TestCase."""

    fixtures = ["country.json"]

    def setUp(self):
        """Proprietaire api testcase setup."""
        self.client = APIClient()
        self.user, created = User.objects.get_or_create(
            first_name="HOUNKANRIN", last_name="Hervé", email="hrvhounkanrin@gmail.com"
        )
        if created:
            self.user.set_password("herve2020")
            self.user.save()
        banque_data = {
            "codebanque": "061",
            "libbanque": "BANK OF ARFICA",
        }
        self.banque = Banque.objects.get_or_create(banque_data)[0]

    def test_proprietaire_can_create(self):
        """Test proprietaire can create."""
        # url = reverse("invoicing_action/get_invoicing", kwargs={"id": id})
        # client.get(url)
        self.client.force_authenticate(user=self.user)
        url = "/api/v1/proprietaire_action/create_proprio"
        proprietaire_data = {
            "mode_paiement": "VIREMENT BANCAIRE",
            "numcompte": "201515454887",
            "banque_id": self.banque.id,
            "pays_residence": "BJ",
        }

        response = self.client.post(url, proprietaire_data, format="json")
        assert response.status_code == 200, "Expect 200 OK. got: {}".format(
            response.status_code
        )
        assert response.json()["payload"]["numcompte"] == "201515454887"
        response = self.client.post(url, proprietaire_data, format="json")
        assert (
            response.status_code == 400
        ), f"Expect 400 OK. got: {response.status_code}"

    def test_proprietaire_cannot_create_if_not_login(self):
        """Test proprietaire can not create if not logged in."""
        url = "/api/v1/proprietaire_action/create_proprio"
        proprietaire_data = {
            "mode_paiement": "VIREMENT BANCAIRE",
            "numcompte": "201515454887",
            "banque_id": self.banque.id,
            "pays_residence": "BJ",
        }
        response = self.client.post(url, proprietaire_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_proprietaire_list(self):
        """Test proprietaire list."""
        self.client.force_authenticate(user=self.user)
        url = "/api/v1/proprietaire_action/get_proprio"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
