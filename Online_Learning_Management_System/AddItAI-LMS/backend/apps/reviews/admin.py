from django.contrib import admin
from .models import Review

# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=["user","course","rating","created_at"]
    search_fields=["user__username","course__title"]
    list_filter=["rating"]
    
