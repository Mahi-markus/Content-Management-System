from django.contrib import admin

from django.contrib import admin
from .models import User, Content, Feedback

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'writter', 'manager', 'created_at', 'updated_at', 'approved_at')
    list_filter = ('status', 'manager')
    search_fields = ('title', 'content', 'writter__username', 'manager__username')
    ordering = ('-created_at',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('content', 'manager', 'comment')
    search_fields = ('content__title', 'manager__username', 'comment')
    ordering = ('-created_at',)
