from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, CharField, ChoiceField, FloatField
from django.forms.widgets import FileInput, Select, TextInput, PasswordInput, EmailInput, NumberInput, Textarea

from django.contrib.auth.models import User
from .models import *

class UserForm(UserCreationForm):
    attrs = {'class': 'form-control', 'id': 'floatingPass', 'placeholder': 'Password', 'required': True}
    password1 = CharField( widget=PasswordInput(attrs=attrs))
    password2 = CharField( widget=PasswordInput(attrs=attrs))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        widgets = {
            'first_name' : TextInput( attrs={'class': 'form-control', 'id': 'floatingFname', 'placeholder': 'First Name', 'required': True}),
            'last_name' : TextInput( attrs={'class': 'form-control', 'id': 'floatingLname', 'placeholder': 'Last Name', 'required': True}),
            'email' : EmailInput( attrs={'type': 'email', 'class': 'form-control', 'id': 'floatingEmail', 'placeholder': 'Email Address', 'required': True}),
            'username' : TextInput( attrs={'class': 'form-control', 'id': 'floatingUsername', 'placeholder': 'username', 'required': True}),
        }

class EditProfile(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']
        widgets = {
            'first_name' : TextInput( attrs={'class': 'form-control', 'id': 'floatingFname', 'placeholder': 'First Name', 'required': True}),
            'last_name' : TextInput( attrs={'class': 'form-control', 'id': 'floatingLname', 'placeholder': 'Last Name', 'required': True}),
            'email' : EmailInput( attrs={'type': 'email', 'class': 'form-control', 'id': 'floatingEmail', 'placeholder': 'Email Address', 'required': True}),
            'username' : TextInput( attrs={'class': 'form-control', 'id': 'floatingUsername', 'placeholder': 'username', 'required': True}),
        }

class EditProfileDetails(ModelForm):
    class Meta:
        model = UserDetails
        fields = ['phone', 'profile_pic']
        widgets = {
            'phone' : TextInput( attrs={'class': 'form-control', 'id': 'floatingPhone', 'placeholder': 'First Name', 'required': False}),
            'profile_pic' : FileInput( attrs={'type' : 'file', 'class': 'form-control', 'id': 'inputProfile_Pic', 'required': False})
        }


class NewRecipe(ModelForm):
    class Meta:
        CHOICES = (('Easy', 'Easy'),('Medium','Medium'),('Hard','Hard'))
        model = Recipe
        fields = ['name', 'difficulty', 'phours', 'pminutes', 'chours', 'cminutes', 'serving', 'equipment', 'ingredients', 'procedures', 'image']
        widgets = {
            'name' : TextInput( attrs={'class': 'form-control', 'id': 'inputName', 'placeholder': 'Dish Name', 'required': True}),
            'difficulty' : Select(choices=CHOICES, attrs={'class': 'form-select', 'id': 'inputDifficulty', 'required': True}),
            'phours' : NumberInput( attrs={'class': 'form-control', 'id': 'inputPhours', 'placeholder': 'Hours', 'required': True}),
            'pminutes' : NumberInput( attrs={'class': 'form-control', 'id': 'inputPmins', 'placeholder': 'Minutes', 'required': True}),
            'chours' : NumberInput( attrs={'class': 'form-control', 'id': 'inputChours', 'placeholder': 'Hours', 'required': True}),
            'cminutes' : NumberInput( attrs={'class': 'form-control', 'id': 'inputCmins', 'placeholder': 'Minutes', 'required': True}),
            'serving' : NumberInput( attrs={'class': 'form-control', 'id': 'inputServing', 'placeholder': 'How many servings', 'required': True}),
            'equipment' : Textarea( attrs={'class': 'form-control', 'id': 'inputEquipment', 'placeholder': 'Cooking utensils needed for the dish', 'required': False}),
            'ingredients' : Textarea( attrs={'class': 'form-control', 'id': 'inputIngredients', 'placeholder': 'Ingredients needed for the dish', 'required': True}),
            'procedures' : Textarea( attrs={'class': 'form-control', 'id': 'inputProcedures', 'placeholder': 'Procedures to cook the dish', 'required': True}),
            'image' : FileInput( attrs={'type' : 'file', 'class': 'form-control', 'id': 'inputImage', 'required': False})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment' : Textarea( attrs={'class': 'form-control', 'id': 'inputComment', 'placeholder': 'What did you think about this recipe?', 'required': False}),
        }

class RatingForm(ModelForm):
    rating = FloatField(max_value=5, min_value=0)
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating' : NumberInput( attrs={'class': 'form-control', 'id': 'inputRating', 'required': True})
        }