from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.site_header = 'How Am I Doing? Admin'

@admin.register(User)
class UserAdmin(UserAdmin):
    pass
