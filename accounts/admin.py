from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User



@admin.register(User)
class CustomeUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff']



