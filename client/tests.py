"""Client app tests."""
import logging
import inspect
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from banque.models import Banque
from client.models import Client
from customuser.models import User

logger = logging.getLogger(__name__)

class ClientAPITestCase(TestCase):
    """Cient API tests."""

    def setUp(self):
        """Initilizing client api test case."""
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
        self.client_data = {
            "id": 0,
            "profession": "Commercante",
            "mode_paiement": "MOMO",
            "ice_contact": "HOUNKANRIN PAULETTE",
            "ice_number": "+22997611897",
            "banque_id": self.banque.id,
            "ice_relation": "string",
            "phone_number": "+22996120534",
            "numero_ifu": "02402952231322",
            "profile_type": "tenant"
        }


    def test_client_can_create(self):
        """Test client can create api."""
        # reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None):
        url = reverse("restapi:root:customuser:auth-login")
        logger.debug(f"Running {inspect.stack()[0][3]} at url {url}")

        self.client.force_authenticate(user=self.user)
        url = "/api/v1/profile_action/create_profile"

        response = self.client.post(url, self.client_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.status_code == 200, "Expect 200 OK. got: {}".format(
            response.status_code
        )
        assert "+22997611897" == response.json()["payload"]["tenant"]["ice_number"]

    def test_client_cannot_create_if_not_login(self):
        """Client client can not test if not log in."""
        url = "/api/v1/profile_action/create_profile"
        response = self.client.post(url, self.client_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_client_cannot_duplicated(self):
        """Test client can not be duplicated."""
        self.client.force_authenticate(user=self.user)
        url = "/api/v1/profile_action/create_profile"
        response_1 = self.client.post(url, self.client_data, format="json")
        assert (
            response_1.status_code == 200
        ), f"Expect 200 OK. got: {response_1.status_code}"
        response_2 = self.client.post(url, self.client_data, format="json")
        assert (
            response_2.status_code == 400
        ), f"Expect 400 OK. got: {response_2.status_code}"

    def test_client_list(self):
        """Test client api list."""
        self.client.force_authenticate(user=self.user)
        url = "/api/v1/client_action/get_client"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
