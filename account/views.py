from django.shortcuts import render, redirect
from .models import Author
from .forms import SignUpForm, LogInForm, ProfileUpdate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def SignUpView(request):
	form = None
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			if len(User.objects.filter(username=cd["username"])) != 0:
				messages.error(request, "Username already exists.")
			else:
				if cd["password1"] == cd["password2"]:
					user1 = Author.objects.create_user(cd["username"], cd["email"], cd["password1"])
					cd = form.cleaned_data
					user1.first_name = "First Name"
					user1.last_name = "Last Name"
					user1.bio = "Bio"
					user1.pic = "author/profile/user-04.jpg"
					user1.save()
					messages.success(request, "Congratulation! You are our new member :)")
				else:
					messages.error(request, "Password and Confirm Password didn't match!")
		else:
			messages.error(request, "Wrong Input")
	else:
		form = SignUpForm()

	return render(request, "account/signup.html", {"form":form})


def LogInView(request):
	form = None
	if request.method == "POST":
		form = LogInForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd["username"], password=cd["password"])
			if user is not None:
				login(request, user)
				messages.success(request, "Successfully Logged In :)")
				return redirect("Blog_list")
			else:
				messages.error(request, "Username/Password is not valid!! :(")
	else:
		form = LogInForm()

	return render(request, "account/login.html", {"form":form})


def LogOutView(request):
	if request.user.is_authenticated:
		logout(request)
		messages.success(request, "Successfully Logged Out :)")
		return redirect("login")
	else:
		messages.error(request, "You are not logged In")
		return redirect("login")


def ProfileView(request, name):
	model = Author.objects.get(username = name)

	return render(request, "account/profile.html", {"model":model})


@login_required
def ProfileUpdateView(request, name):
	form = None
	model = Author.objects.get(username = name)
	if request.method == "POST":
		form = ProfileUpdate(request.POST or None, request.FILES or None, instance=model)
		if form.is_valid():
			cd = form.cleaned_data

			model.first_name = request.POST["first_name"]
			model.last_name = request.POST["last_name"]
			model.bio = request.POST["bio"]
			if model.pic:
				model.pic = request.POST["pic"]
				print(model.pic)
				form.save()
			else:
				model.pic = "author/profile/user-04.jpg"
				print(model.pic)
				form.save()
			messages.success(request, "Successfully Updated Your Profile!")
	else:
		form = ProfileUpdate()

	return render(request, "account/update_profile.html", {"form":form, "model":model})