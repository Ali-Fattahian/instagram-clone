from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Profile


class TestProfile(TestCase):

    def setUp(self):
        self.first_name = "john"
        self.last_name = "doe"
        self.email = "john_doe@gmail.com"
        self.username = "john_doe"
        self.password = "passwordpassword"
        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password)

    def test_create_profile(self):
        """checks if the profile instance was created with the fields required"""
        profile = Profile(username=self.username,
                          password=self.password, email=self.email, user=self.user, first_name=self.first_name, last_name=self.last_name)
        self.assertIsInstance(profile, Profile)

    def test_create_profile_automatically(self):
        """checks the profile is being created automatically by signals"""
        self.assertIsNotNone(self.user.profile)
