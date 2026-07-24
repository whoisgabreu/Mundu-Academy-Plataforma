from django.urls import path
from . import views

urlpatterns = [
    path('guild', views.guild_home, name='guild'),
    path('guild/nova', views.guild_create, name='guild_create'),
    path('g/<slug:slug>', views.community_detail, name='community'),
    path('g/<slug:slug>/editar', views.guild_edit, name='guild_edit'),
    path('g/<slug:slug>/excluir', views.guild_delete, name='guild_delete'),
    path('g/<slug:community_slug>/post/<slug:post_slug>', views.thread_detail, name='thread'),
]
