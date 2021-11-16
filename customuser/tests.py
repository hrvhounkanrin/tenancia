"""Customuser API test case."""
import logging
import inspect
import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import User

logger = logging.getLogger(__name__)

class CustomuserAPITestCase(TestCase):
    """Proprietaire API TestCase."""

    def setUp(self):
        """customuser api testcase setup."""
        self.client = APIClient()
        self.user_data = {
            "first_name": "HOUNKANRIN",
            "last_name": "Hervé",
            "email": "hrvhounkanrin@gmail.com",
            "password": "herve2020",
            "phone_number": "+22996120534",
            "address": "COTONOU",
            "country": "Benin",
            "city": "COTONOU",
            "zip": "",
        }


    def test_user_can_register(self):
        """Test user can register."""
        url = reverse("restapi:root:customuser:users-list")
        logger.debug(f"Running {inspect.stack()[0][3]} at url {url}")

        response = self.client.post(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.status_code == 201, "Expect 201 OK. got: {}".format(
            response.status_code
        )
        self.assertTrue("email" in json.loads(response.content))

    def test_user_can_login(self):
        """Test user can login."""
        url = reverse("restapi:root:customuser:auth-login")
        logger.debug(f"Running {inspect.stack()[0][3]} at url {url}")
        user, created = User.objects.get_or_create(
            first_name="HOUNKANRIN", last_name="Hervé", email="hrvhounkanrin@gmail.com"
        )
        if created:
            user.set_password("herve2020")
            user.save()
        login_payload = {"email": "hrvhounkanrin@gmail.com", "password": "herve2020"}
        response = self.client.post(url, login_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in json.loads(response.content))
