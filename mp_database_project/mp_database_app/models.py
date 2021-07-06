from tkinter import CASCADE
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

def get_deleted_user_instance():
    return User.objects.get(username='deleted-user')

class UserDetails(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	phone = models.CharField(max_length=20, null=True, blank=True)
	profile_pic = models.ImageField(default="default.jpg", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.user.username

class Recipe(models.Model):
	CHOICES = (('Easy', 'Easy'),('Medium','Medium'),('Hard','Hard'))

	author = models.ForeignKey(User, null=True, on_delete=models.SET(get_deleted_user_instance))
	name = models.CharField(max_length=100, null=True)
	difficulty = models.CharField(max_length=6, choices=CHOICES, null=True)
	phours = models.IntegerField(null=True, default=0, validators=[MaxValueValidator(24), MinValueValidator(0)])
	pminutes = models.IntegerField(null=True, default=0, validators=[MaxValueValidator(60), MinValueValidator(0)])
	chours = models.IntegerField(null=True, default=0, validators=[MaxValueValidator(24), MinValueValidator(0)])
	cminutes = models.IntegerField(null=True, default=0, validators=[MaxValueValidator(60), MinValueValidator(0)])
	serving = models.IntegerField(null=True, default=1, validators=[MinValueValidator(1)])
	equipment = models.TextField(blank=True)
	ingredients = models.TextField(blank=True)
	procedures = models.TextField(blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	last_modified = models.DateTimeField(auto_now=False, null=True)
	slug = AutoSlugField(populate_from=["name"])
	image = models.ImageField(default="no_image.jpg", null=True, blank=True)

	def __str__(self):
		return f'{self.name} - {self.author}'

class Comment(models.Model):
	author = models.ForeignKey(User, null=True, on_delete=models.SET(get_deleted_user_instance))
	recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
	comment = models.TextField(max_length=300, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	last_modified = models.DateTimeField(auto_now=False, null=True)

	def __str__(self):
		return f'by {self.author} on "{self.recipe}"'


class Rating(models.Model):
	user = models.ForeignKey(User, null=True, on_delete=models.SET(get_deleted_user_instance))
	recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
	rating = models.FloatField(max_length=300, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return f'by {self.user} on {self.recipe}'

class Favorite(models.Model):
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.user} likes {self.recipe.name}'