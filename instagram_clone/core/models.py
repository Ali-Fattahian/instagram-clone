from django.db import models
from users.models import Profile


class Post(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='post')
    image = models.ImageField()
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f'Post id:{self.id} | author:{self.profile.username}'


class Comment(models.Model):
    content = models.TextField()
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'Comment author: {self.profile.username} | on post: {self.post.id} by: {self.post.profile.username}'


class LikePost(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='profile_like_post')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_like')

    def __str__(self):
        return f'profile {self.profile.username} liked post id {self.post.id} by {self.post.profile.username}'
