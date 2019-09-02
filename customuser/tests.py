from django.test import Client
from django.test import TestCase

from customuser.models import User


class UserAPITestCase(TestCase):
    """
    User API
    """

    def setUp(self):
        self.c = Client()

        self.normal_user = User.objects.create_user(
            username='joe', password='password', email='joe@soap.com')
        self.superuser = User.objects.create_superuser(
            username='clark', password='supersecret', email='joe@soap.com')

    def test_can_get_user_list(self):
        """GET /user returns a list of users"""
        assert False is True

    def test_get_user_returns_correct_fields(self):
        """GET /user/{pk} returns a user"""
        assert False is True

    def test_cannot_create_user_if_not_logged_in(self):
        """POST /user/ returns 401 AUTHENTICATIOD REQUIRED if not logged in"""
        assert False is True

    def test_only_staff_can_create_user(self):
        """POST /user/ returns 403 AUTHENTICATIOD REQUIRED for
a logged in user who is not superuser"""
        assert False is True

    def test_can_create_user_if_logged_in(self):
        """POST /user/ returns 201 CREATED for a valid logged in superuser"""
        assert False is True

    def tearDown(self):
        for user in User.objects.all():
            user.delete()
