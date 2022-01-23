from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestSignUpView(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'testpassword'
        self.email = 'test@gmail.com'
        self.first_name = 'testfirstname'
        self.last_name = 'testlastname'
        self.test_client = Client()

    def test_user_sign_up_form(self):
        """Test the creation of user object by using SignUpView"""
        response = self.test_client.post(reverse('users:sign-up'), data={
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)

        created_user = get_user_model().objects.get(username=self.username)
        self.assertIsInstance(created_user, get_user_model())


class TestLoginView(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'testpassword'
        self.email = 'test@gmail.com'
        self.test_user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email)
        self.test_client = Client()

    def test_login_test_user(self):
        """Test user can log in with username and password using LogInView"""
        self.test_client.post(reverse('users:log-in'), data={
            'username': self.username,
            'password': self.password
        })
        self.assertTrue(self.test_user.is_authenticated)


class TestEditProfileView(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'testpassword'
        self.email = 'test@gmail.com'
        self.first_name = 'testfirstname'
        self.last_name = 'testlastname'

        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email, first_name=self.first_name, last_name=self.last_name)

        self.profile = self.user.profile
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_edit_profile_works(self):
        """Test edit profile url works for a website user"""
        get_response = self.client.get(
            reverse('users:edit-profile', args=[self.profile.slug]))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed('users/profile-edit.html')

    def test_only_user_has_access(self):
        """Test only the user has access to edit profile url specific to that user"""

        test_client = Client()
        get_response_not_auth = test_client.get(
            reverse('users:edit-profile', args=[self.profile.slug]))
        print(get_response_not_auth)

        self.assertEqual(get_response_not_auth.status_code, 403)
