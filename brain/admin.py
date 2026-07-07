from django.contrib import admin
from .models import BrainNote, BrainSavedItem, BrainStreak, BrainFork, BrainFollower


@admin.register(BrainNote)
class BrainNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_public', 'source_type')


@admin.register(BrainSavedItem)
class BrainSavedItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'item_type')


@admin.register(BrainStreak)
class BrainStreakAdmin(admin.ModelAdmin):
    list_display = ('user', 'day', 'active')


@admin.register(BrainFork)
class BrainForkAdmin(admin.ModelAdmin):
    list_display = ('user', 'framework_title', 'uses_my_version')


@admin.register(BrainFollower)
class BrainFollowerAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower_handle', 'since')
