from django.urls import path
from . import views
from .feeds import BlogFeed

urlpatterns = [
			path('', views.Blog_list, name="Blog_list"),
			path('about/', views.AboutView, name="AboutView"),
			# path('popular/', views.PopularView, name="PopularView"),
			path('article/<slug:slug>/update/', views.PostUpdate, name="PostUpdate"),
			path('article/<slug:slug>/delete/', views.PostDelete, name="PostDelete"),
			path('article/<slug:slug>', views.Blog_Detail, name="Blog_Detail"),
			path('post_new/', views.PostNew, name="PostNew"),
			path('category/<slug:category_slug>', views.Blog_list, name="CategoryView"),
			path('author/<slug:author_slug>/', views.Blog_list, name="AuthorView"),
			path('feed/', BlogFeed(), name="BlogFeed"),
			]