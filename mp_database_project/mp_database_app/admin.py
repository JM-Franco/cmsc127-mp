from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(UserDetails)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Favorite)
