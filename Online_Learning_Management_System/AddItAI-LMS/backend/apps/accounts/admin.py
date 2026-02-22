from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ('username','email','role','is_staff','is_superuser')
    list_filter = ('role','is_staff','is_superuser')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info',{
            'fields':('role','bio','profile_image','is_email_verified','is_instructor_approved')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info',{
            'fields':('role','bio','profile_image')
        })
    )

admin.site.register(User,UserAdmin)