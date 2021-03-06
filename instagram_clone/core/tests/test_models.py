from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from core.models import Post, Comment, LikePost


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
        self.test_like_post = LikePost.objects.create(
            profile=self.test_profile, post=self.test_post)

    def test_create_like_post(self):
        """Test likepost object created by profile and post field given"""
        self.assertIsInstance(self.test_like_post, LikePost)


# class TestLikeComment(TestCase):
#     def setUp(self):
#         self.username = 'test_user'
#         self.email = 'test_user@gmail.com'
#         self.password = 'testpassword'
#         self.first_name = 'first test'
#         self.last_name = 'last test'
#         self.test_user = get_user_model().objects.create_user(
#             username=self.username, password=self.password, email=self.email, first_name=self.first_name, last_name=self.last_name)
#         self.test_profile = self.test_user.profile
#         self.test_post = Post.objects.create(content='random string', profile=self.test_profile,
#                                              image='https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg')
#         self.test_comment = Comment.objects.create(
#             content='random string', profile=self.test_profile, post=self.test_post)
#         self.test_like_comment = LikeComment.objects.create(
#             profile=self.test_profile, comment=self.test_comment)

#     def test_create_like_comment(self):
#         """Test likecomment object created by profile and comment field given"""
#         self.assertIsInstance(self.test_like_comment, LikeComment)

class TestLikePostModel(TestCase):
    def setUp(self):
        self.username = 'test_user'
        self.email = 'test_user@gmail.com'
        self.password = 'testpassword'
        self.first_name = 'first test'
        self.last_name = 'last test'
        self.test_user = get_user_model().objects.create_user(
            username=self.username, password=self.password, email=self.email, first_name=self.first_name, last_name=self.last_name)
        self.test_profile = self.test_user.profile
        self.test_post = Post.objects.create(content='random string', profile=self.test_profile,
                                             image='post_images/demo-pic-1.jpg')

        self.username2 = 'test_user2'
        self.email2 = 'test_user2@gmail.com'
        self.password2 = 'testpassword2'
        self.first_name2 = 'first test2'
        self.last_name2 = 'last test2'
        self.test_user2 = get_user_model().objects.create_user(
            username=self.username2, password=self.password2, email=self.email2, first_name=self.first_name2, last_name=self.last_name2)
        self.test_profile2 = self.test_user2.profile

    def test_cant_like_post_more_than_once(self):
        """Test a user can't like another user's post more than once"""
        LikePost.objects.create(
            profile=self.test_profile2, post=self.test_post)
        with self.assertRaises(IntegrityError, msg='Can\'t like the same post twice'):
            LikePost.objects.create(
                profile=self.test_profile2, post=self.test_post)
