from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import Permission
from .models import *


admin.site.register(Permission)
admin.site.register(User)
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("permissions",)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")