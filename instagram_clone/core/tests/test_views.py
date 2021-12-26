from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Post
from users.models import Follow


class TestHomePageView(TestCase):
    def setUp(self):
        self.username1 = 'test_user'
        self.email1 = 'test_user@gmail.com'
        self.password1 = 'testpassword'
        self.first_name1 = 'first test'
        self.last_name1 = 'last test'
        self.test_user1 = get_user_model().objects.create_user(
            username=self.username1, password=self.password1, email=self.email1, first_name=self.first_name1, last_name=self.last_name1)
        self.test_profile1 = self.test_user1.profile
        self.test_post1 = Post.objects.create(content='random string', profile=self.test_profile1,
                                              image='https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg')

        self.username2 = 'test_user2'
        self.email2 = 'test_user2@gmail.com'
        self.password2 = 'testpassword2'
        self.first_name2 = 'first test2'
        self.last_name2 = 'last test2'
        self.test_user2 = get_user_model().objects.create_user(
            username=self.username2, password=self.password2, email=self.email2, first_name=self.first_name2, last_name=self.last_name2)
        self.test_profile2 = self.test_user2.profile

        self.username3 = 'test_user3'
        self.email3 = 'test_user3@gmail.com'
        self.password3 = 'testpassword3'
        self.first_name3 = 'first test3'
        self.last_name3 = 'last test3'
        self.test_user3 = get_user_model().objects.create_user(
            username=self.username3, password=self.password3, email=self.email3, first_name=self.first_name3, last_name=self.last_name3)
        self.test_profile3 = self.test_user3.profile
        self.test_post2 = Post.objects.create(content='random string', profile=self.test_profile3,
                                              image='https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg')

        self.test_follow = Follow.objects.create(
            following_user=self.test_profile2, followed_user=self.test_profile1)

        self.test_client = Client()
        self.test_client.force_login(user=self.test_user2)
        self.response = self.test_client.get(reverse('core:homepage'))

    def test_homepage_view_works(self):
        """Test homepage view returning 200 and rendering the right template"""
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'core/homepage.html')

    def test_posts_shown_in_homepage(self):
        """Test a user can only see the posts from following users"""
        self.assertEqual(self.response.context['posts'].count(), 1)

    def test_comment_form_exist(self):
        """Test CommentForm exist in the homepage view"""
        comment_form = self.response.context.get('comment_form')
        self.assertTrue(comment_form)
        self.assertFalse(self.response.context.get('comment-form'))

    def test_comment_posted(self):
        """Test a comment object created and saved in database"""
        pass
