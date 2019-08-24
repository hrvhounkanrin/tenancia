<<<<<<< HEAD:customuser/tests/user_api_test.py
from django.test import TestCase
from .models import User
=======
from  django.test import Client
from django.test import TestCase

from customuser.models import User
>>>>>>> c920703d4c72c64d8549e783e266def1a9dbad36:customuser/tests.py
class UserAPITestCase(TestCase):

    """
    User API
    """

    def setUp(self):
        self.c = Client()

        self.normal_user = User.objects.create_user(
<<<<<<< HEAD:customuser/tests/user_api_test.py
            username="joe", password="password", email="joe@gmail.com")
        self.superuser = User.objects.create_superuser(
            username="hrvhounkanrin", password="supersecret", email="hrvhounkanrin@gmail.com")
=======
            username='joe', password='password', email='joe@soap.com')
        self.superuser = User.objects.create_superuser(
            username='clark', password='supersecret', email='joe@soap.com')
>>>>>>> c920703d4c72c64d8549e783e266def1a9dbad36:customuser/tests.py

    def test_can_get_user_list(self):
       """GET /user returns a list of users"""
        url = reverse("user_api")
        print('Url reversed: {}'.format(url))
        response = self.c.get(url)

        assert response.status_code == 200, \
            "Expect 200 OK. got: {}" . format(response.status_code)
        num_users = len(response.json())

        assert num_users == 2, \
            "Expect it to return exactly 2 users. Got: {}" . format(num_users)
    
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
