from django.db import models
from django.contrib.auth.models import User

class Author(User):
	pic = models.FileField(upload_to="author/profile")
	bio = models.TextField()
	fb = models.URLField(null=True, blank=True)
	tw = models.URLField(null=True, blank=True)
	ins = models.URLField(null=True, blank=True)
	web = models.URLField(null=True, blank=True)