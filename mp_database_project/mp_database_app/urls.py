from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipe/<slug:slug>', views.recipe, name='recipe'),
    path('search_results/', views.search_results, name="search_results"),
    path('add_recipe/', views.add_recipe, name="add_recipe"),
    path('profile/<str:username>', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('edit_comment/<str:pk>', views.edit_comment, name='edit_comment'),
    path('edit_recipe/<slug:slug>', views.edit_recipe, name='edit_recipe'),
    path('delete_recipe/<str:pk>', views.delete_recipe, name='delete_recipe'),
    path('add_fav/<str:pk>', views.add_fav, name='add_fav'),
    # path('add_comment/<str:pk>', views.add_comment, name='add_comment'),
    path('delete_comment/<str:pk>', views.delete_comment, name='delete_comment'),
    path('login_user/', views.login_user, name='login_user'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout')
]