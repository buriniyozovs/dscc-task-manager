from django.contrib import admin
from .models import Category, Task, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['user']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'deadline', 'status', 'created_at']
    list_filter = ['status', 'priority', 'categories']
    search_fields = ['title', 'description']
    filter_horizontal = ['categories']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'created_at']
    list_filter = ['created_at']