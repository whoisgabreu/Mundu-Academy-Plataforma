from django.urls import path
from . import api

urlpatterns = [
    path('post/<slug:post_id>/vote', api.vote_post, name='api_vote_post'),
    path('comment/<slug:comment_id>/vote', api.vote_comment, name='api_vote_comment'),
    path('post', api.create_post, name='api_create_post'),
    path('comment', api.create_comment, name='api_create_comment'),
    path('community/<slug:slug>/join', api.join_community, name='api_join_community'),
    path('follow/<slug:handle>', api.follow_user, name='api_follow_user'),
    path('framework/<slug:framework_id>/fork', api.fork_framework, name='api_fork_framework'),
    path('framework/<slug:framework_id>/review', api.review_framework, name='api_review_framework'),
    path('share-to-guild', api.share_to_guild, name='api_share_to_guild'),
    path('note/<slug:note_id>/toggle-public', api.toggle_note_public, name='api_toggle_note_public'),
    path('notifications', api.list_notifications, name='api_list_notifications'),
    path('notifications/read-all', api.read_all_notifications, name='api_read_all_notifications'),
    path('notifications/<slug:notif_id>/read', api.read_notification, name='api_read_notification'),
    path('quick-note', api.quick_note, name='api_quick_note'),
    path('progresso', api.update_progress, name='api_update_progress'),
    path('desafio/<int:desafio_id>/completar', api.complete_challenge, name='api_complete_challenge'),
    path('xp', api.my_xp, name='api_my_xp'),
    path('quiz/<int:quiz_id>/submit', api.submit_quiz, name='api_submit_quiz'),
]
