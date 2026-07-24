from django.contrib import admin
from .models import Community, Thread, Comment, Vote, GuildMembership, GuildMission, GuildMissionProgress


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'members', 'nivel', 'xp_total', 'missions_completed', 'posts_today')
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


@admin.register(GuildMembership)
class GuildMembershipAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'community', 'role', 'xp', 'joined_at')
    list_filter = ('role', 'community')
    search_fields = ('usuario__username', 'community__name')


@admin.register(GuildMission)
class GuildMissionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'community', 'meta', 'xp', 'ativo')
    list_filter = ('ativo', 'community')


@admin.register(GuildMissionProgress)
class GuildMissionProgressAdmin(admin.ModelAdmin):
    list_display = ('membership', 'mission', 'progresso', 'concluida')
    list_filter = ('concluida', 'mission__community')
