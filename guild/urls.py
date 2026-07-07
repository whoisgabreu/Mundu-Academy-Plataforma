from django.urls import path
from . import views

urlpatterns = [
    path('guild', views.guild_home, name='guild'),
    path('g/<slug:slug>', views.community_detail, name='community'),
    path('g/<slug:community_slug>/post/<slug:post_slug>', views.thread_detail, name='thread'),
]
