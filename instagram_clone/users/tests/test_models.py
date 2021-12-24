from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Profile, Follow


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


class TestFollowModel(TestCase):
    def setUp(self):
        self.username1 = 'test_user'
        self.email1 = 'test_user@gmail.com'
        self.password1 = 'testpassword'
        self.first_name1 = 'first test'
        self.last_name1 = 'last test'
        self.test_user1 = get_user_model().objects.create_user(
            username=self.username1, password=self.password1, email=self.email1, first_name=self.first_name1, last_name=self.last_name1)
        self.test_profile1 = self.test_user1.profile

        self.username2 = 'test_user2'
        self.email2 = 'test_user2@gmail.com'
        self.password2 = 'testpassword2'
        self.first_name2 = 'first test2'
        self.last_name2 = 'last test2'
        self.test_user2 = get_user_model().objects.create_user(
            username=self.username2, password=self.password2, email=self.email2, first_name=self.first_name2, last_name=self.last_name2)
        self.test_profile2 = self.test_user2.profile

        self.test_follow = Follow.objects.create(
            following_user=self.test_profile2, followed_user=self.test_profile1)

    def test_create_follow(self):
        """Test follow object created by follower and following field given """
        self.assertIsInstance(self.test_follow, Follow)

    def test_check_users_followers(self):
        """Check following users exist in followed user 'follow section'"""
        self.assertEqual(self.test_profile2.followings.all()[0].id, self.test_profile1.id)
        self.assertEqual(self.test_profile1.followers.count(), 1)