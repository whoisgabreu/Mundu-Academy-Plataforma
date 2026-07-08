from django.contrib import admin
from .models import Community, Thread, Comment, Vote


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'members', 'posts_today')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'author_handle', 'upvotes', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_handle', 'thread', 'upvotes', 'created_at')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'valor', 'content_type', 'object_id', 'created_at')
