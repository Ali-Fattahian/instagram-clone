from django import forms
from .models import Comment, LikePost, SavePost


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 0, 'cols': 0})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update(
            {'placeholder': 'Add a comment...'})


class LikePostForm(forms.ModelForm):
    class Meta:
        model = LikePost
        fields = tuple()


class SavePostForm(forms.ModelForm):
    class Meta:
        model = SavePost
        fields = tuple()
