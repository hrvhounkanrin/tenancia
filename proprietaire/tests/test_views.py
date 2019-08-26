from django.test import TestCase, Client
from rest_framework.response import Response
from rest_framework import status
from customuser.models import User
class ViewsetsTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.normal_user = User.objects.get_or_create(
            username="herve", password="herve", email="hrvhounkanrin@gmail.com",
             "first_name"="Herve", "last_name"="HOUNKANRIN")


    def test_proprietaire_can_create(self):
        data = {
                "proprietaire":[
                    {
                        "mode_paiement": "VIREMENT BANCAIRE",
                        "numcompte": "201515454887",
                        "banque_id":2,
                        "pays_residence": "BJ",
                        "user_id":2
                    }
                ]
            }
        url = reverse("user-list")
        response = self.c.post(url, data)
        assert response.status_code == 403, \
            "Expect 403 AUTHENTICATION REQUIRED. got: {}" . format(
                response.status_code)
        assert User.objects.count() == 2, \
        	'Expect no new users to have been created'


    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)