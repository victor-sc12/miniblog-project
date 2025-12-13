from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Inlines:
class BloggerProfileInline(admin.StackedInline):
    """This inline is not being used for the moment"""
    model = BloggerProfile


# Register your models here:
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Rol personalizado', {'fields': ('is_blogger',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('is_blogger', )}),
    )

# admin.site.register(User)
admin.site.register(BloggerProfile)
