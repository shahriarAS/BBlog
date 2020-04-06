from django.contrib import admin
from .models import Category, BlogPost, Comment

class CategoryAdmin(admin.ModelAdmin):
	list_display = ["title", "slug"]
	list_filters = ["title", "slug"]
	search_fields = ['title', "slug"]

	prepopulated_fields = {"slug":("title", )}

admin.site.register(Category, CategoryAdmin)


class BlogPostAdmin(admin.ModelAdmin):
	list_display = ["id", "title", "author", "category", "created_at", "status"]
	list_filters = ["title", "author" "created_at", "status"]
	search_fields = ["title", "author", "category", "created_at", "status", "body"]
	list_editable = ["status", "title", "category", "author"]

	prepopulated_fields = {"slug":("title", )}

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Comment)