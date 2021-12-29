from django import forms
from .models import Comment, LikePost


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class LikePostForm(forms.ModelForm):
    class Meta:
        model = LikePost
        fields = tuple()