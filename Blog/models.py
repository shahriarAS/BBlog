from django.db import models
from django.contrib.auth.models import User
from account.models import Author
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import ArrayField


STATUS = (("Draft", "Draft"), ("Publish", "Publish"))


class Category(models.Model):
	title = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.title

class BlogPost(models.Model):
	title = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	body = RichTextUploadingField()
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	thumbnail = models.FileField(upload_to="Blog/thumb")
	tag = ArrayField(models.CharField(max_length=50, blank=True), default=list)
	status = models.CharField(choices = STATUS, default="Draft", max_length=200)
	updated_at = models.DateTimeField(auto_now=True)
	count = models.IntegerField(editable = False, default=0)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	email = models.EmailField()
	body = RichTextUploadingField()
	created_at = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name = "reply")

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return self.name