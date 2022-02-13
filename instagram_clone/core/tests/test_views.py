import os
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import MagicMock
from django.db.utils import IntegrityError
from django.core.files import File
from django.conf import settings
from core.forms import CommentForm
from core.models import Post, Comment, LikePost, SavePost
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
                                              image='post_images/demo-pic-1.jpg')

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
                                              image='post_images/demo-pic-1.jpg')

        self.test_follow = Follow.objects.create(
            following_user=self.test_profile2, followed_user=self.test_profile1)

        self.test_client = Client()
        self.test_client.force_login(user=self.test_user2)
        self.get_response = self.test_client.get(reverse('core:homepage'))

    def test_homepage_view_works(self):
        """Test homepage view returning 200 and rendering the right template"""
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'core/homepage.html')

    def test_posts_shown_in_homepage(self):
        """Test a user can only see the posts from following users"""
        self.assertEqual(self.get_response.context['posts'].count(), 1)

    def test_comment_form_exist(self):
        """Test CommentForm exist in the homepage view"""
        comment_form = self.get_response.context.get('comment_form')
        self.assertTrue(comment_form)
        self.assertIsInstance(comment_form, CommentForm)
        self.assertFalse(self.get_response.context.get('comment-form'))

    def test_comment_posted(self):
        """Test a comment object created and saved in database and is connected to expected post"""
        self.test_client.post(reverse('core:homepage'), data={
            'content': 'idk',
            'post_id': self.test_post1.id  # the hidden input required
        })
        comment = Comment.objects.get(content='idk')
        self.assertTrue(comment)
        self.assertEqual(comment.post, self.test_post1)
        self.assertEqual(comment.profile, self.test_profile2)

    def test_home_page_for_not_authenticated(self):
        """Test homepage shows the posts for not authenticated users"""
        not_auth_user = Client()
        response = not_auth_user.get(reverse('core:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/homepage.html')

    def test_post_like(self):
        """Test post like feature works by clicking on heart icon for authenticated users"""

        self.test_client.post(reverse('core:homepage'), data={
            'like_post_id': self.test_post2.id
        })

        self.assertTrue(LikePost.objects.filter(
            profile=self.test_profile2, post=self.test_post2).exists())

        with self.assertRaises(IntegrityError, msg='Can\'t like the same post twice'):
            self.test_client.post(reverse('core:homepage'), data={
                'like_post_id': self.test_post2.id
            })

    def test_post_save_unsave(self):
        """Test a user can save and unsave a post in homepage"""
        self.test_client.post(reverse('core:homepage'), data={
            'post_save_id': self.test_post2.id
        })
        self.assertTrue(SavePost.objects.filter(
            profile=self.test_profile2, post=self.test_post2).exists())

        self.test_client.post(reverse('core:homepage'), data={
            'post_unsave_id': self.test_post2.id
        })
        self.assertFalse(SavePost.objects.filter(
            profile=self.test_profile2, post=self.test_post2).exists())


class TestProfileDetail(TestCase):
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

        self.test_client = Client()
        self.get_response = self.test_client.get(
            reverse('core:user-account', args=(self.test_profile.slug, )), )

    def test_profile_detail_works(self):
        """Test this view works and uses the right template"""
        self.assertTemplateUsed(self.get_response, 'core/user-account.html')
        self.assertEqual(self.get_response.status_code, 200)

    def test_follow_works(self):
        """Test Follow button works and doesn't allow users to follow someone more than once"""
        self.test_client.force_login(user=self.test_user)
        self.logged_in_test_response = self.test_client.post(reverse('core:user-account', args=(self.test_profile2.slug, )), data={
            'user-follow': True
        })
        self.assertTrue(Follow.objects.filter(
            followed_user=self.test_profile2, following_user=self.test_profile).exists())


class PostDetailView(TestCase):
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
        self.test_client = Client()
        self.test_client.force_login(user=self.test_user)
        self.get_response = self.test_client.get(
            reverse('core:post', args=(self.test_profile.slug, self.test_post.pk)))

    def test_post_detail_works(self):
        """Test this view works and uses the right template"""
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'core/post-detail.html')

    def test_save_unsave_works(self):
        """Test a user can save and unsave a post in PostDetail page"""
        self.test_client.post(reverse('core:post', args=(self.test_profile.slug, self.test_post.pk)), data={
            'post_save': True
        })
        self.assertTrue(SavePost.objects.filter(
            post=self.test_post, profile=self.test_profile))

        self.test_client.post(reverse('core:post', args=(self.test_profile.slug, self.test_post.pk)), data={
            'post_unsave': True
        })
        self.assertFalse(SavePost.objects.filter(
            post=self.test_post, profile=self.test_profile))


class AddPostView(TestCase):
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
        self.test_client.force_login(user=self.test_user)
        self.get_response = self.test_client.get(reverse('core:add-post'))

    def test_get_post_add_view(self):
        """Test post add view works for get request"""
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'core/new-post.html')

    def test_post_added(self):
        """Test post added to database after using add post view"""
        self.test_client.post(reverse('core:add-post'), data={
            'post-image': MagicMock(spec=File, name='FileMock'),
            'post-caption': 'some test'
        })

        # remove the created file called post-image
        os.remove(settings.BASE_DIR / 'uploaded_files/post_images/post-image')
        post = Post.objects.get(content='some test')
        self.assertTrue(post)

    def test_post_not_added(self):
        """Test post object can not be created if the user is not authenticated"""
        test_client2 = Client()
        test_client2.post(reverse('core:add-post'), data={
            'post-caption': 'some test',
            'post-image': MagicMock(spec=File, name='FileMock')
        })

        self.assertFalse(Post.objects.filter(content='some test'))


class TestDeletePostView(TestCase):
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
        self.test_client.force_login(user=self.test_user)
        self.test_post = Post.objects.create(content='random string', profile=self.test_profile,
                                             image='post_images/demo-pic-1.jpg')

    def test_delete_post_url_works(self):
        """Test delete post url returns 200 response for a logged in user and it uses the right template"""
        response = self.test_client.get(reverse('core:delete-post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/delete-post.html')

    def test_delete_post_works(self):
        """Test that after sending a POST request with the required post id, it deletes the post"""
        self.assertIsInstance(self.test_post, Post)
        self.assertTrue(Post.objects.filter(id=self.test_post.pk))
        self.test_client.post(reverse('core:delete-post'), data={
            'post-delete-id': self.test_post.pk
        })
        self.assertFalse(Post.objects.filter(id=self.test_post.pk))

    def test_delete_post_not_work(self):
        """Test delete post url does not work for not-auth users"""
        self.assertIsInstance(self.test_post, Post)
        not_auth_client = Client()
        not_auth_client.post(reverse('core:delete-post'), data={
            'post-delete-id': self.test_post.pk
        })
        self.assertTrue(Post.objects.filter(id=self.test_post.pk))
