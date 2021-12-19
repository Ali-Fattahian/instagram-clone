from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class Profile(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile")
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    bio = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username} | {self.email}'


class Follow(models.Model):
    followed_user = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="followers")
    following_user = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="followings")

    def __str__(self):
        return f'followed user:{self.followed_user}, following user:{self.following_user}'
