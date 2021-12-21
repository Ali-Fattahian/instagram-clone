from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Post, Comment


class TestPostModel(TestCase):

    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@gmail.com'
        self.password = 'testpassword'
        self.first_name = 'first test'
        self.last_name = 'last test'
        self.test_user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email, first_name=self.first_name, last_name=self.last_name,)
        self.test_profile = self.test_user.profile
        self.test_post = Post.objects.create(content='random string', profile=self.test_profile,
                                             image='https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg')

    def test_create_post(self):
        """Test the creation of a post with content, profile and image given"""
        self.assertIsInstance(self.test_post, Post)


class TestCommentModel(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@gmail.com'
        self.password = 'testpassword'
        self.first_name = 'first test'
        self.last_name = 'last test'
        self.test_user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email, first_name=self.first_name, last_name=self.last_name,)
        self.test_profile = self.test_user.profile
        self.test_post = Post.objects.create(content='random string', profile=self.test_profile,
                                             image='https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg')
        self.test_comment = Comment.objects.create(
            content='random string', profile=self.test_profile, post=self.test_post)

    def test_create_comment(self):
        """Test the creation of a comment with content, profile and post given"""
        self.assertIsInstance(self.test_comment, Comment)

    def test_comment_field(self):
        """Test if the value inside of each field equals the expected """
        self.assertEqual(self.test_comment.profile, self.test_profile)
        self.assertEqual(self.test_comment.post, self.test_post)
        self.assertEqual(self.test_comment.content, 'random string')


class TestLikePostModel(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@gmail.com'
        self.password = 'testpassword'
        self.first_name = 'first test'
        self.last_name = 'last test'
        self.test_user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email, first_name=self.first_name, last_name=self.last_name,)
        self.test_profile = self.test_user.profile
        self.test_post = Post.objects.create(content='random string', profile=self.test_profile,
                                             image='https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg')
        self.test_comment = Comment.objects.create(
            content='random string', profile=self.test_profile, post=self.test_post)
        self.test_like_post = LikePost.objects.create(
            profile=self.test_profile, post=self.test_post)

    def test_create_like_post(self):
        """Test likepost object created by profile and post field given"""
        self.assertIsInstance(self.test_like_post, LikePost)
