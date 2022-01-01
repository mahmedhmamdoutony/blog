from django.contrib import admin
from .models import Post,Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_date', 'created_by']
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','is_active','comment_date']

