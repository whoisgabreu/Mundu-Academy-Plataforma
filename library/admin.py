from django.contrib import admin
from .models import Summary, Framework, FrameworkReview


@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tag', 'saves')


@admin.register(Framework)
class FrameworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'uses', 'rating')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(FrameworkReview)
class FrameworkReviewAdmin(admin.ModelAdmin):
    list_display = ('author_handle', 'framework', 'rating', 'helpful')
