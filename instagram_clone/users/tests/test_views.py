from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class TestSignUpView(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'testpassword'
        self.email = 'test@gmail.com'
        self.first_name = 'testfirstname'
        self.last_name = 'testlastname'
        self.test_client = Client()

    def test_sign_up_user(self):
        """Test the creation of user object by using sign up view"""
        response = self.test_client.post('/users/sign-up', {'username': self.username, 'password': self.password,
                                         'email': self.email, 'first_name': self.first_name, 'last_name': self.last_name})
        self.assertEqual(response.status_code, 200)
