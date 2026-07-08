from django.contrib import admin
from .models import Follow, Notification


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['seguidor', 'seguido', 'created_at']
    search_fields = ['seguidor__username', 'seguido__username']
    list_filter = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'mensagem', 'lida', 'created_at']
    list_filter = ['tipo', 'lida']
    search_fields = ['usuario__username', 'mensagem']
