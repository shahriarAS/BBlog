from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import BlogPost
from django.urls import reverse



class BlogFeed(Feed):
	title = "BBlog RSS FEED"
	link = "/blog/"
	description = "All Latest Article Of BBlog"

	def items(self):
		return BlogPost.objects.filter(status="Publish").order_by("-created_at")

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return truncatewords(item.body, 30)

	# def item_link(self, item):
	# 	return reverse("BlogFeed", args=[item.id])