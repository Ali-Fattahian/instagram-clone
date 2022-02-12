from django.db import models
import datetime
from users.models import Profile
from .utils import *


class Post(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='post_images/')
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f'Post id:{self.id} | author:{self.profile.username}'

    @property
    def date_created_clean(self):
        now = datetime.datetime.now()
        now_aware = now.replace(tzinfo=datetime.timezone.utc) #Add UTC to add similar to django datetimefield default behavior
        return datetime_subtractor(now_aware, self.date_created)

    @property
    def date_created_ago_format(self):
        """A property that shows creation date and time of a post in 'ago' format"""
        return datetime_generator(self.date_created_clean, self.date_created)

    class Meta:
        ordering = ['-date_created']

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'post'], name='Can\'t like same the post twice'
            )
        ]

    def __str__(self):
        return f'profile {self.profile.username} liked post id {self.post.id} by {self.post.profile.username}'


# class LikeComment(models.Model):
#     profile = models.ForeignKey(
#         Profile, on_delete=models.CASCADE, related_name='profile_like_comment')
#     comment = models.ForeignKey(
#         Comment, on_delete=models.CASCADE, related_name='comment_like')

#     def __str__(self):
#         return f'profile {self.profile.username} liked comment id {self.comment.id} by {self.comment.profile.username}'
# Commented out because of some weird bugs caused after handling so many different request.POST types in homepage and post-detail page

class SavePost(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='saved_posts')

    def __str__(self):
        return f'Profile {self.profile.username} saved post id {self.post.id} by {self.post.profile.username}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'post'], name='You can\'t save the same post more than once'),
        ]