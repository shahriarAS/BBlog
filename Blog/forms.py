from django import forms
from .models import BlogPost, Comment

class NewPostForm(forms.ModelForm):
	class Meta:
		model = BlogPost
		fields = ["title", "slug", "body", "status", "category", "thumbnail", "tag"]

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ["name", "email", "body"]