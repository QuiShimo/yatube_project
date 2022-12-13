from django import forms

from posts.models import Comments, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
