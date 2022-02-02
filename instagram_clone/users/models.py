from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse


class Profile(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile")
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    bio = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to='profile_pictures/', blank=True, default='profile_pictures/default_profile_picture.png')
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:edit-profile', args=[self.slug])
    
    def __str__(self):
        return f'{self.username} | {self.email}'


class Follow(models.Model):
    followed_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="followers")
    following_user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="followings")

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(followed_user=models.F(
                'following_user')), name='A follow object with the same following and followed user can not be created'),
            models.UniqueConstraint(fields=[
                                    'followed_user', 'following_user'], name='Can\'t follow the same user more than once')
        ]

    def __str__(self):
        return f'followed user:{self.followed_user}, following user:{self.following_user}'
