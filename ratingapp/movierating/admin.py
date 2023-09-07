from django.contrib import admin

# Register your models here.
from .models import User, Movie, UserProfile
# Register your models here.

admin.site.register(User)
admin.site.register(Movie)
admin.site.register(UserProfile)
