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

    def test_clean_email(self):
        """Test an email including uppercase letters automatically saves into the database with lowercase letters"""
        email = 'TEST@gmail.com'
        self.test_client.post(reverse('users:sign-up'), data={
            'username': self.username,
            'email': email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password1': self.password,
            'password2': self.password
        })
        created_user = get_user_model().objects.get(username=self.username)
        self.assertEqual(created_user.email, 'test@gmail.com')  # TEST --> test


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
        self.assertTemplateUsed(get_response, 'users/profile-edit.html')

    def test_only_user_has_access(self):
        """Test only the user has access to edit profile url specific to that user"""

        test_client = Client()
        get_response_not_auth = test_client.get(
            reverse('users:edit-profile', args=[self.profile.slug]))
        print(get_response_not_auth)

        self.assertEqual(get_response_not_auth.status_code, 403)


class TestProfileListView(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@gmail.com'
        self.password = 'testpassword'
        self.first_name = 'first test'
        self.last_name = 'last test'
        self.test_user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email, first_name=self.first_name, last_name=self.last_name)
        self.test_profile = self.test_user.profile

        self.test_client = Client()

    def test_profile_list_view(self):
        """Test profile list view for showing search results works(get request) and shows the right template"""
        response = self.test_client.get(reverse('users:search-results'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile-list.html')

    def test_search_profile_username(self):
        """Test searching(post request) with username shows the right result in ProfileList page"""

        username = 'new user'
        first_name = 'new user firstname'
        last_name = 'new user lastname'
        email = 'newemail@gmail.com'
        password = 'newuser1234'
        user = get_user_model().objects.create_user(username=username, password=password,
                                                    first_name=first_name, last_name=last_name, email=email)
        response = self.test_client.post(reverse('users:search-results'), data={
            'search_query': 'te'  # i expect to see test_user as result because of username
        })

        # There is duplicate data in context so context[0]
        self.assertTrue(self.test_profile in response.context[0]['profiles'])
        self.assertFalse(user.profile in response.context[0]['profiles'])


class TestProfileDeleteConfirm(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@gmail.com'
        self.password = 'testpassword'
        self.first_name = 'first test'
        self.last_name = 'last test'
        self.test_user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email, first_name=self.first_name, last_name=self.last_name)
        self.test_profile = self.test_user.profile

        self.test_client = Client()
        self.test_client.force_login(self.test_user)

    def test_profile_delete_works(self):
        """Test profile delete confirmation page shows up for a logged in user"""
        response = self.test_client.get(reverse('users:profile-delete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'users/profile-delete-confirmation.html')
