from django import forms
from .models import Post


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "status", "category")
