from django import forms

from posts.models import PostAttachment


class PostForm(forms.ModelForm):
    class Meta:
        model = PostAttachment
        fields = "__all__"
