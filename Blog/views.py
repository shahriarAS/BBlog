from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import BlogPost, Category, Comment
from .forms import NewPostForm, CommentForm
from account.models import Author
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.forms import inlineformset_factory


all_post = BlogPost.objects.filter(status="Publish").order_by("-created_at")

category = Category.objects.all()


def Blog_list(request, category_slug=None, author_slug=None):
	
	all_post = BlogPost.objects.filter(status="Publish").order_by("-created_at")
	query = request.GET.get("q", None)

	
	if query != None:
		model = BlogPost.objects.filter(body__contains=query)
		is_featured = False
		header = None
	elif category_slug == None and author_slug == None:
		model = BlogPost.objects.filter(status="Publish").order_by("-created_at")
		is_featured = True
		header = None
	elif category_slug:
		category_id = Category.objects.get(slug=category_slug)
		model = BlogPost.objects.filter(category=category_id).order_by("-created_at")
		is_featured = False
		header = "category"

	elif author_slug:
		author_id = Author.objects.get(username=author_slug)
		model = BlogPost.objects.filter(author=author_id).order_by("-created_at")
		is_featured = False
		header = "author"
	


	pagination = Paginator(model, 9)

	page_number = request.GET.get('page')

	page_obj = pagination.get_page(page_number)

	context = {
			"all_post":all_post,
			"category":category,
			"model":model,
			"is_featured":is_featured,
			"page_obj":page_obj,
			"author_slug":author_slug,
			"category_slug":category_slug,
			"header":header
				}

	return render(request, "Blog/index.html", context)


def Blog_Detail(request, slug):
	post = BlogPost.objects.get(slug=slug)
	auth = Author.objects.get(username = post.author)
	
	post.count += 1
	post.save()

	req_user = str(request.user)
	post_author = str(post.author)

	comments = Comment.objects.filter(post=post, active=True, parent__isnull=True)

	reply_comment = Comment.objects.filter(post=post, parent__isnull=False)

	if request.method == "POST":
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			parent_obj = None
			try:
				parent_id = int(request.POST.get("parent_id"))
			except:
				parent_id = None

			if parent_id:
				parent_obj = Comment.objects.get(id=parent_id)
				if parent_obj:
					reply_comment = comment_form.save(commit=False)
					reply_comment.parent = parent_obj
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
			return redirect("Blog_Detail", post.slug)
	else:
		comment_form = CommentForm()


	return render(request, "Blog/Post_View.html", {"reply_comment":reply_comment, "comments":comments, "comment_form":comment_form, "all_post":all_post, "req_user":req_user, "post_author":post_author, "auth":auth, "post":post, "category":category})


def AboutView(request):

	return render(request, "Blog/about.html", {"all_post":all_post, "category":category})

def PostNew(request):
	form = None
	auth = Author.objects.get(username=request.user)
	if auth.pic:
		if request.method == "POST":
			form = NewPostForm(request.POST, request.FILES)
			if form.is_valid():
				cd = form.cleaned_data
				post = form.save(commit=False)
				post.created_at = timezone.now()
				post.author = auth
				post.updated_at = timezone.now()
				post.title = request.POST["title"]
				post.slug = request.POST["slug"]
				if auth.is_staff == True:
					post.status = request.POST["status"]
					post.save()
					messages.success(request, "You're Post has been published. :)")
					print(messages)
				else:
					post.status = "Draft"
					post.save()
					messages.info(request, "You're Post has been sent for moderation. After moderate you will enter into our writer panel & you will informed. :)")
					print(messages)
			else:
				print("Not Valid Post")
				print(form.errors)
				
		else:
			form = NewPostForm()
	else:
		messages.info(request, "Please Complete Your profile!!")
		form = NewPostForm()

	return render(request, "Blog/post_new.html", {"all_post":all_post, "category":category, "form":form})


def PostDelete(request, slug):
	post = BlogPost.objects.get(slug=slug)

	if str(request.user) == str(model.author):
		if request.method == "POST":
			model.delete()
			messages.success(request, "Successfully Deleted The Post !")
			return redirect("Blog_list")
		return render(request, "Blog/post_delete.html", {"all_post":all_post, "post":post, "category":category})


def PostUpdate(request, slug):
	form = None
	auth = Author.objects.get(username=request.user)
	model = BlogPost.objects.get(slug=slug)
	form = NewPostForm(request.POST or None, request.FILES or None, instance=model)
	if form.is_valid():
		form.save()
	else:
		print("Hoini")

	return render(request, "Blog/edit.html", {"all_post":all_post, "form":form, "model":model})



# def SearchView(request):
# 	query = request.GET.get(q, None)
# 	if query != None:
# 		model = BlogPost.objects.filter(body_contains=query)

# 	return render