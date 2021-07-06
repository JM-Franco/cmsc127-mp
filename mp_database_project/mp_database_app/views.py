from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

from datetime import datetime
# Create your views here.

def home(request):
	return render(request, 'mp_database_app/home.html')

@login_required(login_url="/register")
def recipes(request):
	
	if(request.method == "POST"):
		search = request.POST.get('search')
		if search:
			search_q = search.split()
			for q in search_q:
				recipes = (Recipe.objects.filter(name__contains=q) or Recipe.objects.filter(ingredients__contains=q) or Recipe.objects.filter(difficulty__contains=q))
			data = {"search":search, "recipes":recipes}
			return render(request, 'mp_database_app/recipes.html', data)
		else:
			recipes = Recipe.objects.all()
			data = {"search":search, "recipes":recipes}
	recipes = Recipe.objects.all()
	data = {"recipes":recipes}
	return render(request, 'mp_database_app/recipes.html', data)

def recipe(request, slug):
	recipe = Recipe.objects.get(slug=slug)
	comments = recipe.comment_set.all()
	commentform = CommentForm()
	if(request.user.is_authenticated):
		if(request.method == "POST"):
			commentform = CommentForm(request.POST)
			if(commentform.is_valid()):
				instance = commentform.save(commit=False)
				instance.author = request.user
				instance.recipe = recipe
				instance.save()
				return redirect(request.path)

	if request.user.is_authenticated:
		favorites = Favorite.objects.filter(user=request.user, recipe=recipe)
		data = {"recipe":recipe, "comments":comments, "commentform":commentform, "favorites":favorites}
	else:
		data = {"recipe":recipe, "comments":comments, "commentform":commentform}
	return render(request, 'mp_database_app/recipe.html', data)

def search_results(request):
	if(request.method == "POST"):
		search = request.POST.get('search')
		if (request.user.is_authenticated):
			if search:
				search_q = search.split()
				for q in search_q:
					recipes = Recipe.objects.filter(name__contains=q) or (Recipe.objects.filter(ingredients__contains=q)) or (Recipe.objects.filter(difficulty__contains=q))
					return render(request, 'mp_database_app/search_results.html', {'searched':search, 'results':recipes})
			else:
				recipes = Recipe.objects.all()
				return render(request, 'mp_database_app/search_results.html', {'searched':search, 'results':recipes})
		else:
			if search:
				recipes = Recipe.objects.filter(name__contains=search)
				return render(request, 'mp_database_app/search_results.html', {'searched':search, 'results':recipes})
			else:
				recipes = Recipe.objects.all()
				return render(request, 'mp_database_app/search_results.html', {'searched':search, 'results':recipes})
				
		
	return render(request, 'mp_database_app/search_results.html')

@login_required(login_url='/register')
def add_fav(request, pk):
	request.session['previous'] = request.META.get('HTTP_REFERER', '/')
	q = Favorite.objects.filter(user=request.user, recipe=Recipe.objects.get(id=pk))
	if (q.exists()):
		instance = Favorite.objects.get(user=request.user, recipe=Recipe.objects.get(id=pk))
		instance.delete()
	else:
		instance = Favorite(user=request.user, recipe=Recipe.objects.get(id=pk))
		instance.save()
	return HttpResponseRedirect(request.session['previous'])


@login_required(login_url='/register')
def add_recipe(request):
	form = NewRecipe()
	if(request.method == "POST"):
		form = NewRecipe(request.POST, request.FILES)
		if(form.is_valid()):
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			messages.success(request, "Recipe Published")
			return redirect("/recipes")
	data = {"form":form}
	return render(request, 'mp_database_app/add_recipe.html', data)

@login_required(login_url='/register')
def edit_recipe(request, slug):
	recipe = Recipe.objects.get(slug=slug)
	if(request.method == "POST"):
		form = NewRecipe(request.POST, request.FILES, instance=recipe)
		if(form.is_valid()):
			recipe.slug = None
			recipe.last_modified = datetime.now()
			form.save()
			messages.success(request, "Recipe edit success")
			return redirect('/recipes')

	form = NewRecipe(instance=recipe)
	data = {"form":form}
	return render(request, 'mp_database_app/edit_recipe.html', data)

# @login_required(login_url='/register')
# def add_comment(request):
# 	request.session['previous'] = request.META.get('HTTP_REFERER', '/')
# 	if(request.method == "POST"):
# 		commentform = CommentForm(request.POST)
# 		if(commentform.is_valid()):
# 			instance= commentform.save(commit=False)
# 			instance.author = request.user
# 			instance.recipe = recipe
# 			instance.save()
# 			return HttpResponseRedirect(request.session['previous'])
# 	return HttpResponseRedirect(request.session['previous'])
		

@login_required(login_url='/register')
def edit_comment(request, pk):
	comment = Comment.objects.get(id=pk)
	if(request.method == "GET"):
		request.session['previous'] = request.META.get('HTTP_REFERER', '/')
	elif(request.method == "POST"):
		form = CommentForm(request.POST, instance=comment)
		if(form.is_valid()):
			comment.last_modified = datetime.now()
			form.save()
			messages.success(request, "Comment edit success")
			return HttpResponseRedirect(request.session['previous'])
			# return redirect(previous_page)

	form = CommentForm(instance=comment)
	data = {"form":form}
	return render(request, 'mp_database_app/edit_comment.html', data)

@login_required(login_url='/register')
def profile(request, username):
	user = User.objects.get(username=username)
	userdetails = UserDetails.objects.get(user=user)
	recipes = user.recipe_set.all()
	comments = user.comment_set.all()
	favorites = Favorite.objects.filter(user=user)
	data = {"user":user, "userdetails": userdetails, "recipes":recipes, "comments":comments, "favorites":favorites}
	return render(request, 'mp_database_app/profile.html', data)

@login_required(login_url="/register")
def edit_profile(request):
	user = request.user
	userdetails = UserDetails.objects.get(user=request.user.pk)
	if(request.method == "POST"):
		userform = EditProfile(request.POST, instance=user)
		userdetailform = EditProfileDetails(request.POST, request.FILES, instance=userdetails)
		if(userform.is_valid() and userdetailform.is_valid()):
				userform.save()
				userdetailform.save()
				messages.success(request, "Account edit success")
				return redirect(reverse('profile', kwargs={"username": user.username}))

	userform = EditProfile(instance=user)
	userdetailform = EditProfileDetails(instance=userdetails)
	data = {"userform":userform, "userdetailform":userdetailform}
	return render(request, 'mp_database_app/edit_profile.html', data)

def login_user(request):
	request.session['previous'] = request.META.get('HTTP_REFERER', '/')
	if(request.method == "POST"):
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			print("login success")
			messages.success(request, "Login successfully.")
			return redirect("/")
		else:
			print("login fail")
			messages.error(request, "Incorrect password or username.")

	return HttpResponseRedirect(request.session['previous'])


def register(request):
	if request.user.is_authenticated:
		return redirect("/")
	else:
		form = UserForm()

		if(request.method == "POST"):
			form = UserForm(request.POST)
			if(form.is_valid()):
				user = form.save()
				userdetails = UserDetails(user=user)
				login(request, user)

				messages.success(request, "Account created for "+form.cleaned_data.get("username"))
				return redirect("/")

		data = {"form":form}
		return render(request, 'mp_database_app/register.html', data)

@login_required(login_url="/")
def logout_user(request):
	logout(request)
	return redirect("/")


@login_required(login_url="/")
def delete_comment(request,pk):
	request.session['previous'] = request.META.get('HTTP_REFERER', '/')
	comment = Comment.objects.get(id=pk)
	comment.delete()
	return HttpResponseRedirect(request.session['previous'])

@login_required(login_url="/")
def delete_recipe(request,pk):
	recipe = Recipe.objects.get(id=pk)
	recipe.delete()
	return redirect("/recipes")